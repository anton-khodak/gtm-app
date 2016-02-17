import pandas as pd
from daterange_filter.filter import DateRangeFilter
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django_pandas.io import read_frame
from push_notifications.admin import DeviceAdmin
from push_notifications.models import APNSDevice, GCMDevice

from constants.excel import export_to_xls
from constants.helper_functions import translate_column_names, translit
from users.models import *


class GTMAdminSite(AdminSite):
    site_header = 'Администрация GTM'


class UserProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('score', 'total_score', 'total_exchange')
    fieldsets = [
        ('Личные данные', {'fields': ['user', 'patronimyc', 'gender', 'age', 'date_of_birth', 'area', 'city']}),
        ('Контактная информация', {'fields': ['main_phone', 'secondary_phone', 'work_phone']}),
        ('Работа',
         {'fields': ['work', 'position', 'speciality', 'category', 'curing_form', 'bed_quantity', 'patient_quantity']}),
        ('Адрес для корреспонденции', {'fields': ['district', 'house', 'flat', 'index']}),
        ('Баланс', {'fields': ['score', 'total_score', 'total_exchange']}),
    ]


class UserFilterAdmin(admin.ModelAdmin):
    model = UserFilter
    actions = ['export_to_xls_users']

    def export_to_xls_users(self, request, queryset):
        df = pd.DataFrame()
        for el in queryset:
            users = el.get_filtered_user_queryset()
            df = pd.concat([df, read_frame(users,
                            index_col='user__id',
                            verbose=True,
                            fieldnames=(
                            'user__id', 'user__username', 'user__first_name', 'user__last_name', 'patronimyc',
                            'user__email', 'date_of_birth', 'age', 'gender', 'city__name', 'area__name',
                            'score', 'total_score',
                            'total_exchange',
                            'speciality__name',
                            'work__name', 'curing_form', 'position__name', 'category', 'bed_quantity',
                            'patient_quantity',
                            'main_phone', 'secondary_phone', 'work_phone',
                            'district', 'house', 'flat', 'index',))])
        df = translate_column_names(df)
        return export_to_xls(df, translit(el.name) + '.xls')

    export_to_xls_users.short_description = "Выгрузить информацию о группе пользователей в xls"



class UserChangeHistoryAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'exchange', 'date',)
    list_filter = [('day', DateRangeFilter)]
    actions = ['export_to_xls_exchange']

    def export_to_xls_exchange(self, request, queryset):
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
                             'exchange' +
                             request.GET.get('drf__day__gte ', '') +
                             request.GET.get('drf__day__lte', '') + '.xls',
                             engine='openpyxl')
    export_to_xls_exchange.short_description = 'Выгрузить информацию об обменах в xls'


admin_site = GTMAdminSite(name='admin')
admin_site.register(UserProfile, UserProfileAdmin)
admin_site.register(UserExchangeHistory, UserChangeHistoryAdmin)
admin_site.register(User, UserAdmin)
admin_site.register(UserFilter, UserFilterAdmin)
admin_site.register(APNSDevice, DeviceAdmin)
admin_site.register(GCMDevice, DeviceAdmin)
