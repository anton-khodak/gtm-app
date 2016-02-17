import datetime as dt
from push_notifications.models import APNSDevice, GCMDevice

from django import forms
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet, Count
from django_pandas.io import read_frame
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from constants.excel import export_to_xls
from constants.helper_functions import translate_column_names, translit
from polls.models import *
from users.admin import admin_site


class AnswerInline(NestedStackedInline):
    model = Answer
    fk_name = 'level'
    list_display = ['answer_text', 'next_question']
    fields = ['answer_text', 'next_question']


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'answer_text', 'next_question']
    fields = ['question', 'answer_text', 'next_question']


class QuestionInline(NestedStackedInline):
    model = Question
    inlines = [AnswerInline]
    fields = ['text', 'question_text']
    fk_name = 'level'
    list_display = ('question_text', 'poll')


class PollForm(forms.ModelForm):
    def save(self, commit=True):
        self.instance.save()
        user_group = self.instance.user_group
        if user_group:
            users = user_group.get_filtered_user_queryset()
        else:
            users = UserProfile.objects.all()
        for user in users:
            try:
                UsersPoll.objects.get(poll=self.instance, user=user)
            except ObjectDoesNotExist:
                userspoll = UsersPoll(poll=self.instance,
                                      user=user,
                                      date_assigned=datetime.datetime.now(),
                                      date_passed=datetime.datetime.now(),
                                      passed=False)
                userspoll.save()
                print(userspoll)
        devices = GCMDevice.objects.filter(user__pk__in=users.values_list('pk'))
        devices.send_message("Новый опрос {0}".format(self.instance.name))
        return super(PollForm, self).save(commit=commit)

    class Meta:
        fields = '__all__'
        model = Poll


class PollAdmin(NestedModelAdmin):
    model = Poll
    inlines = [QuestionInline]
    form = PollForm
    fk_name = 'level'
    list_filter = ['users']
    filter_horizontal = ['users']
    actions = ['export_to_xls_poll']

    fieldsets = [
        (None, {'fields': ['name', 'score', 'poll_type', 'user_group', 'medicine', 'additional']}),
        # ('Пользователи', {'fields': ['gender', 'age_from', 'age_to',]}),

    ]

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
                percent = answers/total_counts*100
            else:
                percent = 0
            df.ix[i, 'percent'] = str(percent)+'%'
        i = dt.datetime.now()
        path = 'oprosy' + "_%s_%s_%s" % (i.day, i.month, i.year) + '.xls'
        df = translate_column_names(df)
        return export_to_xls(df, path)

    export_to_xls_poll.short_description = 'Выгрузить опросы в xls'


class UsersPollAdmin(admin.ModelAdmin):
    list_filter = ['user']
    actions = ['unpass_polls']

    def unpass_polls(self, request, queryset):
        rows_updated = queryset.update(passed=False)
        if rows_updated == 1:
            message_bit = "1 опрос"
        else:
            message_bit = "%s опросов" % rows_updated
        self.message_user(request, "%s отмечены как непройденные." % message_bit)

    unpass_polls.short_description = 'Отметить опросы как непройденные'


class UserAnswerAdmin(admin.ModelAdmin):
    model = UserAnswer
    list_filter = ['user']


class UserPollFilterAdmin(admin.ModelAdmin):
    model = UserPollFilter
    actions = ['export_to_xls_user_poll']

    def export_to_xls_user_poll(self, request, queryset):
        uf = queryset[0]
        users = uf.get_filtered_user_queryset()
        if not uf.polls:
            uf.polls = Poll.objects.all()
        polls = UsersPoll.objects.filter(user__pk__in=users.values_list('pk'),
                                         poll__pk__in=uf.polls.values_list('pk'), )
        if uf.date_from:
            polls = polls.filter(date_passed__lte=uf.date_from)
        if uf.date_to:
            polls = polls.filter(date_passed__gte=uf.date_to)
        polls = Poll.objects.filter(pk__in=polls.values_list('poll'))
        answers = UserAnswer.objects.filter(user__pk__in=users.values_list('pk'),
                                            question__poll__pk__in=polls.values_list('pk'))
        answers = answers.order_by(uf.order, set(ORDERS - set(uf.order)).pop(), 'question__id', 'answer__id')
        df = read_frame(answers,
                        verbose=True,
                        fieldnames=(
                            'user__user__id', 'user__user__username',
                            'question__poll__id', 'question__poll__name',
                            'question__id', 'question__question_text',
                            'answer__id', 'answer__answer_text',
                            'other_answer',
                        ))
        df = translate_column_names(df)
        return export_to_xls(df, translit(uf.name) + '.xls', engine='openpyxl')

    export_to_xls_user_poll.short_description = 'Выгрузить опросы пользователей в xls'


admin_site.register(Question)
admin_site.register(Answer, AnswerAdmin)
admin_site.register(Poll, PollAdmin)
admin_site.register(UsersPoll, UsersPollAdmin)
admin_site.register(UserAnswer, UserAnswerAdmin)
admin_site.register(PollAdditional)
admin_site.register(UserPollFilter, UserPollFilterAdmin)
