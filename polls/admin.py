import datetime as dt

import pandas as pd
from ajax_select.fields import AutoCompleteSelectMultipleField
from django import forms
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.utils.safestring import mark_safe
from django_pandas.io import read_frame
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from push_notifications.models import APNSDevice, GCMDevice

from constants.excel import export_to_xls
from constants.helpers import translate_column_names, translit, LoggerFactory, append_user_m2m_fields, unique_chain
from polls.models import *
from users.admin import admin_site


logger = LoggerFactory.get_logger(__name__)


class AnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # populates "next_question" queryset only with questions related to the poll
        super(AnswerForm, self).__init__(*args, **kwargs)
        try:
            self.fields['next_question'].queryset = Question.objects.filter(poll=self.instance.question.poll)
        except AttributeError:
            pass

    class Meta:
        fields = '__all__'
        model = Answer


class AnswerInline(NestedStackedInline):
    model = Answer
    extra = 1
    fk_name = 'level'
    list_display = ['answer_text', 'next_question']
    fields = ['answer_text', 'next_question']
    form = AnswerForm


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'answer_text', 'next_question']
    fields = ['question', 'answer_text', 'next_question']


class AnswerTranslatedAdmin(AnswerInline, TranslationStackedInline):
    pass


class QuestionInline(NestedStackedInline):
    model = Question
    extra = 1
    inlines = [AnswerTranslatedAdmin]
    fields = ['text', 'question_text']
    fk_name = 'level'
    list_display = ('question_text', 'poll')


class QuestionTranslatedNestedAdmin(QuestionInline, TranslationStackedInline):
    pass


class TranslatedQuestionAdmin(TranslationAdmin):
    pass


class PollForm(forms.ModelForm):
    send_notification = forms.BooleanField(label="Отправить уведомления", required=False)
    separate_users = AutoCompleteSelectMultipleField('separate_users', required=False, help_text='Отдельные пользователи')

    class Meta:
        fields = '__all__'
        model = Poll

    def save(self, commit=True):
        self.instance.save()
        self._save_m2m()
        # TODO: if field.has_changed()
        # тут можна оптимізувати перевіркою, чи змінювалася група або окремі користувачі
        # так само з історіями
        users = self.instance.get_all_related_users()
        if users:
            for user in users:
                try:
                    UsersPoll.objects.get(poll=self.instance, user=user)
                except ObjectDoesNotExist:
                    UsersPoll.objects.create(poll=self.instance,
                                             user=user,
                                             date_assigned=timezone.now(),
                                             date_passed=timezone.now(),
                                             passed=False)

        if self.data.get('send_notification', ''):
            if type(users) is list:
                users_value_list = set(user.pk for user in users)
            else:
                users_value_list = users.values_list('pk')
            userspolls = UsersPoll.objects.filter(poll=self.instance, user__pk__in=users_value_list,
                                                  notification_sent=False)
            # new_users - користувачі, яким ще не відправлялося сповіщення
            new_users = UserProfile.objects.filter(pk__in=userspolls.values_list('user__pk'))
            android_devices = GCMDevice.objects.filter(user__pk__in=new_users.values_list('pk'))
            ios_devices = APNSDevice.objects.filter(user__pk__in=new_users.values_list('pk'))
            try:
                android_devices.send_message("Новый опрос: {0}".format(self.instance.name))
            except Exception as e:
                logger.exception("Failed to sent message to GCM device {0}".format(self.instance.name))
                pass
            try:
                ios_devices.send_message("Новый опрос: {0}".format(self.instance.name))
            except Exception as e:
                logger.exception("Failed to sent message to APNS device {0}".format(self.instance.name))
                pass
            userspolls.update(notification_sent=True)
        self.instance.change_date = timezone.now()
        return super(PollForm, self).save(commit=commit)


class PollAdmin(NestedModelAdmin, admin.ModelAdmin):
    model = Poll
    inlines = [QuestionTranslatedNestedAdmin]
    extra = 1
    form = PollForm
    fk_name = 'level'
    list_filter = ['poll_type']
    list_display = ['name', 'change_date']
    readonly_fields = ['change_date', 'related_groups', 'related_separate_users', 'related_histories']
    list_select_related = True
    filter_horizontal = ['user_group', 'histories']
    actions = ['export_to_xls_poll']

    fieldsets = [
        (None, {'fields': ['name', 'poll_type', 'user_group', 'separate_users',
                           'medicine', 'additional', 'change_date', 'send_notification']}),
        ('Ссылки', {'fields': ['histories', 'related_groups', 'related_separate_users', 'related_histories']}),
    ]

    class Media:
        js = ('js/jquery.min.js',
              'rest_framework/js/own.js',)

    def related_groups(self, obj):
        string = ''
        for uf in obj.user_group.all():
            string += '<a href="{}">{}</a><br>'.format(
                reverse("admin:users_userfilter_change", args=(uf.pk,)),
                uf.name)
        return mark_safe(string)

    related_groups.short_description = 'Группы, которые получили опрос'

    def related_separate_users(self, obj):
        string = ''
        for up in obj.separate_users.all():
            string += '<a href="{}">{}</a><br>'.format(
                reverse("admin:users_userprofile_change", args=(up.pk,)),
                up.user.username)
        return mark_safe(string)

    related_separate_users.short_description = 'Отдельные пользователи, которые получили опрос'

    def related_histories(self, obj):
        string = ''
        for history in obj.histories.all():
            string += '<a href="{}">{}</a><br>'.format(
                reverse("admin:history_pollhistory_change", args=(history.pk,)),
                history.name)
        return mark_safe(string)

    related_histories.short_description = 'Связанные истории'

    def export_to_xls_poll(self, request, queryset):
        qs = None
        for poll in queryset:
            if qs:
                qs |= Answer.objects.filter(question__poll=poll.id)
            else:
                qs = Answer.objects.filter(question__poll=poll.id)
        qs = qs.annotate(useranswers=Count('useranswer'))
        qs = qs.order_by('-question__poll__id', 'question__id', 'id')
        df = read_frame(qs,
                        verbose=True,
                        fieldnames=('question__poll__id',
                                    'question__poll__name',
                                    'question__id',
                                    'question__question_text',
                                    'id',
                                    'answer_text',
                                    'useranswers'
                                    ))
        for i, row in df.iterrows():
            question = df.loc[i, 'question__id']
            answers = df.loc[i, 'useranswers']
            total_counts = sum(df[df['question__id'] == question]['useranswers'])
            if total_counts:
                percent = answers / total_counts * 100
            else:
                percent = 0
            df.ix[i, 'percent'] = str(percent) + '%'
        i = dt.datetime.now()
        path = 'oprosy' + "_%s_%s_%s" % (i.day, i.month, i.year) + '.xls'
        df = translate_column_names(df)
        return export_to_xls(df, path)
    export_to_xls_poll.short_description = 'Выгрузить опросы в xls'


class TranslatedPollAdmin(PollAdmin, TranslationAdmin):
    pass


class UsersPollAdminForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=UserProfile.objects.select_related('user').all(),
                                  required=False,
                                  help_text='Пользователь')

    class Meta:
        model = UsersPoll
        fields = '__all__'


class UsersPollAdmin(admin.ModelAdmin):
    list_filter = ['passed', 'date_assigned', 'date_passed', 'poll', ]
    search_fields = ['user__user__username', 'poll__name']
    actions = ['unpass_polls', 'export_poll_to_xls']
    form = UsersPollAdminForm

    def unpass_polls(self, request, queryset):
        for el in queryset:
            if el.passed:
                UserAnswer.objects.filter(user=el.user, question__poll=el.poll).delete()
        rows_updated = queryset.update(passed=False)
        if rows_updated == 1:
            message_bit = "1 опрос"
        else:
            message_bit = "%s опросов" % rows_updated
        self.message_user(request, "%s отмечены как непройденные, ответы пользователей удалены." % message_bit)

    unpass_polls.short_description = 'Отметить опросы как непройденные'

    def export_poll_to_xls(self, request, queryset):
        df = read_frame(queryset, verbose=True, fieldnames=('user', 'poll', 'passed'))
        return export_to_xls(df, 'poll.xls')

    def get_queryset(self, request):
        qs = UsersPoll.objects.select_related('user__user').select_related('poll').all()
        return qs


class UserAnswerForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=UserProfile.objects.select_related('user').all(),
                                  required=False)

    class Meta:
        model = UserAnswer
        fields = '__all__'


class UserAnswerAdmin(admin.ModelAdmin):
    model = UserAnswer
    form = UserAnswerForm
    search_fields = ['user__user__username']

    def get_queryset(self, request):
        qs = UserAnswer.objects.select_related('user__user').select_related('question').select_related('answer').all()
        return qs


class UserPollFilterForm(forms.ModelForm):
    users = AutoCompleteSelectMultipleField('separate_users', required=False, help_text='Отдельные пользователи')

    class Meta:
        model = UserPollFilter
        fields = '__all__'


class UserPollFilterAdmin(admin.ModelAdmin):
    model = UserPollFilter
    actions = ['export_to_xls_user_poll']
    filter_horizontal = ['polls',]
    form = UserPollFilterForm

    def export_to_xls_user_poll(self, request, queryset):
        result_queryset = []
        for uf in queryset:
            users = uf.get_filtered_user_queryset()
            if not uf.polls.all():
                uf.polls = Poll.objects.all()
            users_polls = UsersPoll.objects.filter(user__pk__in=users.values_list('pk'),
                                                   poll__pk__in=uf.polls.values_list('pk'), )
            if uf.date_from:
                users_polls = users_polls.filter(date_passed__gte=uf.date_from)
            if uf.date_to:
                users_polls = users_polls.filter(date_passed__lte=uf.date_to)
            polls = Poll.objects.filter(pk__in=users_polls.values_list('poll'))
            answers = UserAnswer.objects.filter(user__pk__in=users.values_list('pk'),
                                                question__poll__pk__in=polls.values_list('pk'))
            answers = answers.order_by(uf.order, set(ORDERS - set(uf.order)).pop(), 'question__id', 'answer__id')
            users_passed = read_frame(answers,
                                      verbose=True,
                                      fieldnames=(
                                          'user__user__id', 'user__user__username', 'user__user__first_name',
                                          'user__user__last_name', 'user__gender', 'user__area',
                                          'user__city', 'user__curing_form', 'user__category',
                                          'question__poll__id', 'question__poll__name',
                                          'question__id', 'question__question_text',
                                          'answer__id', 'date_answered', 'answer__answer_text', 'other_answer',
                                      ))
            # вивантажуємо також дані про користувачів, які не пройшли опитування
            users_polls = users_polls.filter(passed=False).order_by('user__user__username')
            users_not_passed = read_frame(users_polls,
                                          verbose=True,
                                          fieldnames=(
                                              'user__user__id', 'user__user__username', 'user__user__first_name',
                                              'user__user__last_name', 'user__gender',
                                              'user__area', 'user__city', 'user__curing_form', 'user__category',
                                              'date_assigned',
                                              'poll__name'
                                          ))
            users_not_passed.rename(columns={'poll__name': 'question__poll__name'}, inplace=True)
            df = users_passed.append(users_not_passed)
            result_queryset.append(df)
        df = pd.concat(result_queryset, keys=range(len(result_queryset)))

        # Ставимо колонки у зворотньому порядку
        df = df[df.columns[::-1]]
        # Вставляємо в інформацію про користувачів спеціальність та інші m2m поля
        df = append_user_m2m_fields(df, 'user__user__id', 'user__category')
        # ставимо в кінець колонку "other answer"
        columns = list(df.columns.values)
        columns.remove('other_answer')
        columns.append('other_answer')
        df = df[columns]
        # даємо людські імена колонкам
        df = translate_column_names(df)
        return export_to_xls(df, translit(queryset[0].__str__()) + '.xls')

    export_to_xls_user_poll.short_description = 'Выгрузить опросы пользователей в xls'

    def get_queryset(self, request):
        qs = UserPollFilter.objects.select_related('group').all()
        return qs


# admin_site.register(Question, TranslatedQuestionAdmin)
# admin_site.register(Answer, AnswerAdmin)
admin_site.register(Poll, TranslatedPollAdmin)
admin_site.register(UsersPoll, UsersPollAdmin)
admin_site.register(UserAnswer, UserAnswerAdmin)
admin_site.register(PollAdditional)
admin_site.register(UserPollFilter, UserPollFilterAdmin)
