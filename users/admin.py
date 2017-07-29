import pandas as pd
from ajax_select.admin import AjaxSelectAdmin
from ajax_select.fields import AutoCompleteSelectMultipleField, AutoCompleteSelectField
from daterange_filter.filter import DateRangeFilter
from django import forms
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.admin.helpers import ActionForm
from django.contrib.auth.admin import UserAdmin
from django.core.urlresolvers import reverse
from django.db.models import Count, Sum
from django.utils.safestring import mark_safe
from django_pandas.io import read_frame
from push_notifications.admin import DeviceAdmin
from push_notifications.models import APNSDevice, GCMDevice

from constants.excel import export_to_xls
from constants.helpers import translate_column_names, translit, append_user_m2m_fields
from users.models import *


class GTMAdminSite(AdminSite):
    site_header = 'Администрация GTM'


class UserForm(forms.ModelForm):
    area = AutoCompleteSelectField('area', required=False, help_text='Область')
    city = AutoCompleteSelectField('city', required=False, help_text='Город')

    def save(self, commit=True):
        self.instance.save(update_groups=True)
        return super(UserForm, self).save(commit=commit, )

    class Meta:
        fields = '__all__'
        model = UserProfile


class UserProfileAdmin(AjaxSelectAdmin, admin.ModelAdmin):
    form = UserForm
    list_display = ['get_username', 'get_last_name', 'get_first_name', 'get_specialities',
                    'category', 'get_positions', 'get_last_login']
    filter_horizontal = ['additional_speciality', 'works', 'positions']
    readonly_fields = ['score', 'total_score', 'total_exchange',
                       'related_groups', 'related_text_polls', 'related_simple_polls', 'related_histories',
                       'get_last_name', 'get_first_name', 'get_last_login']
    fieldsets = [
        ('Личные данные', {'fields': ['user', 'get_last_name', 'get_first_name', 'patronimyc', 'get_last_login', 'gender', 'age', 'date_of_birth', 'area', 'city']}),
        ('Контактная информация', {'fields': ['main_phone', 'secondary_phone', 'work_phone']}),
        ('Работа',
         {'fields': ['works', 'positions', 'additional_speciality', 'category', 'curing_form', 'bed_quantity', 'patient_quantity']}),
        ('Адрес для корреспонденции', {'fields': ['district', 'house', 'flat', 'index']}),
        # derprecated
        # ('Баланс', {'fields': ['score', 'total_score', 'total_exchange', ]}),
        ('Связанное', {'fields': ['related_groups', 'related_text_polls', 'related_simple_polls', 'related_histories']})
    ]
    search_fields = ['user__username']
    ordering = ('-user_id', )
    change_list_template = 'pagination_on_top.html'

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'additional_speciality':
            kwargs['queryset'] = Speciality.objects.order_by('name')
        elif db_field.name == 'works':
            kwargs['queryset'] = Hospital.objects.order_by('name')
        elif db_field.name == 'positions':
            kwargs['queryset'] = Position.objects.order_by('name')
        return super(UserProfileAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def related_groups(self, obj):
        string = ''
        for uf in obj.userfilter_set.all():
            string += '<a href="{}">{}</a><br>'.format(
                reverse("admin:users_userfilter_change", args=(uf.pk,)),
                uf.name)
        return mark_safe(string)
    related_groups.short_description = 'Группы пользователя'

    def related_text_polls(self, obj):
        string = ''
        for uf in obj.userspoll_set.filter(poll__poll_type='text'):
            string += '<a href="{}">{}</a><br>'.format(
                reverse("admin:polls_poll_change", args=(uf.poll.pk,)),
                uf.poll.name)
        return mark_safe(string)
    related_text_polls.short_description = 'Текстовые опросы'

    def related_simple_polls(self, obj):
        string = ''
        for uf in obj.userspoll_set.filter(poll__poll_type='simple'):
            string += '<a href="{}">{}</a><br>'.format(
                reverse("admin:polls_poll_change", args=(uf.poll.pk,)),
                uf.poll.name)
        return mark_safe(string)
    related_simple_polls.short_description = 'Простые опросы'

    def related_histories(self, obj):
        string = ''
        for uf in obj.userhistory_set.all():
            string += '<a href="{}">{}</a><br>'.format(
                reverse("admin:history_pollhistory_change", args=(uf.poll.pk,)),
                uf.poll.name)
        return mark_safe(string)
    related_histories.short_description = 'Истории'

    def get_queryset(self, request):
        qs = UserProfile.objects.select_related('user').all()
        return qs

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Логин'

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'Имя'

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Фамилия'

    def get_specialities(self, obj):
        return ", ".join([str(p) for p in obj.additional_speciality.all()])
    get_specialities.short_description = 'Специальности'

    def get_positions(self, obj):
        return ", ".join([str(p) for p in obj.positions.all()])
    get_positions.short_description = 'Должности'

    def get_last_login(self, obj):
        return obj.user.last_login
    get_last_login.short_description = 'Последний вход'


class SendTextNotificationActionForm(ActionForm):
    text = forms.CharField(required=False)


class UserFilterForm(forms.ModelForm):
    users = AutoCompleteSelectMultipleField('separate_users', required=False, help_text='Отдельные пользователи')

    class Meta:
        fields = '__all__'
        model = UserFilter


class UserFilterAdmin(admin.ModelAdmin):
    form = UserFilterForm
    action_form = SendTextNotificationActionForm
    actions = ['export_to_xls_users', "send_bulk_message_to_all_users"]
    filter_horizontal = ['speciality', 'work', 'position', 'area', 'city', ]
    readonly_fields = ['get_users']
    change_list_template = 'pagination_on_top.html'

    def export_to_xls_users(self, request, queryset):
        df = pd.DataFrame()
        for el in queryset:
            users = el.get_filtered_user_queryset()
            users = users.annotate(userlogins=Count('usersession'))
            users = users.annotate(usertime=Sum('usersession__duration'))

            df = pd.concat([df, read_frame(users,
                                           index_col='user__id',
                                           verbose=True,
                                           fieldnames=(
                                               'user__id', 'user__username', 'user__first_name', 'user__last_name',
                                               'patronimyc',
                                               'user__email', 'user__last_login', 'userlogins', 'usertime',
                                               'date_of_birth', 'age', 'gender', 'city__name', 'area__name',
                                               # 'score', 'total_score', 'total_exchange',
                                               'curing_form', 'category',
                                               'bed_quantity',
                                               'patient_quantity',
                                               'main_phone', 'secondary_phone', 'work_phone',
                                               'district', 'house', 'flat', 'index',))])
        df.reset_index(level=0, inplace=True)
        df = append_user_m2m_fields(df, 'user__id', 'area__name')
        df = translate_column_names(df)
        return export_to_xls(df, translit(el.name) + '.xls', engine='openpyxl')
    export_to_xls_users.short_description = "Выгрузить информацию о группе пользователей в xls"

    def send_bulk_message_to_all_users(self, request, queryset):
        for el in queryset:
            android_devices = GCMDevice.objects.filter(user__pk__in=el.users.values_list('pk'))
            ios_devices = APNSDevice.objects.filter(user__pk__in=el.users.values_list('pk'))
            android_devices.send_message(request.POST.get('text', ''))
            ios_devices.send_message(request.POST.get('text', ''))
    send_bulk_message_to_all_users.short_description = 'Отправить сообщение всем пользователям'

    def get_queryset(self, request):
        qs = UserFilter.objects.prefetch_related('users__user').all()
        return qs

    def get_users(self, obj):
        string = ''
        for user in obj.get_filtered_user_queryset():
            string += '<a href="{}">{}</a>, '.format(
                reverse("admin:users_userprofile_change", args=(user.pk,)),
                user.user.username)
        return mark_safe(string)
    get_users.short_description = 'Пользователи в группе'


class UserChangeHistoryAdmin(admin.ModelAdmin):
    """ deprecated """
    readonly_fields = ('user', 'exchange', 'date',)
    list_filter = [('date', DateRangeFilter), 'user']
    actions = ['export_to_xls_exchange']

    def export_to_xls_exchange(self, request, queryset):
        return UserChangeHistoryAdmin.exchange_to_xls(queryset,
                                               request.GET.get('drf__day__gte ', ''),
                                               request.GET.get('drf__day__lte', ''),
                                               )

    export_to_xls_exchange.short_description = 'Выгрузить информацию об обменах в xls'

    @staticmethod
    def exchange_to_xls(queryset, day_from='_', day_to='_', send=False):
        df = read_frame(queryset,
                        index_col='date',
                        verbose=True,
                        fieldnames=(
                            'date',
                            'user__user__id', 'user__user__username',
                            'user__user__email',
                            'exchange',
                            'user__score', 'user__total_score',
                            'user__total_exchange',
                        ))
        df = translate_column_names(df)
        return export_to_xls(df,
                             'exchange' + day_from
                             + '_' + day_to + '.xls',
                             engine='openpyxl', send=send)


class UserSessionAdminForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=UserProfile.objects.select_related('user').all())

    class Meta:
        model = UserSession
        fields = '__all__'


class UserSessionAdmin(admin.ModelAdmin):
    model = UserSession
    list_filter = [('time', DateRangeFilter)]
    actions = ['export_to_xls_session']
    form = UserSessionAdminForm
    search_fields = ['user__user__username']

    def get_queryset(self, request):
        qs = UserSession.objects.select_related('user__user').all()
        return qs

    def export_to_xls_session(self, request, queryset):
        df = read_frame(queryset,
                        verbose=True,
                        fieldnames=(
                            'user__user__id', 'user__user__username',
                            'duration',
                            'time',
                        ))
        df = translate_column_names(df)
        return export_to_xls(df,
                             'user_session' +
                             request.GET.get('drf__day__gte ', '') +
                             request.GET.get('drf__day__lte', '') + '.xls',
                             engine='openpyxl')

    export_to_xls_session.short_description = 'Выгрузить информацию о сессиях в xls'



admin_site = GTMAdminSite(name='admin')
admin_site.register(UserProfile, UserProfileAdmin)
# admin_site.register(UserExchangeHistory, UserChangeHistoryAdmin)
admin_site.register(User, UserAdmin)
admin_site.register(UserFilter, UserFilterAdmin)
admin_site.register(UserSession, UserSessionAdmin)

# admin_site.register(APNSDevice, DeviceAdmin)
# admin_site.register(GCMDevice, DeviceAdmin)
