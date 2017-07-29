from ajax_select.fields import AutoCompleteSelectMultipleField
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin

from constants.helpers import LoggerFactory, unique_chain
from history.models import *
from polls.models import Poll
from users.admin import admin_site

logger = LoggerFactory.get_logger(__name__)


class HistoryForm(forms.ModelForm):
    separate_users = AutoCompleteSelectMultipleField('separate_users', required=False,
                                                     help_text='Отдельные пользователи')

    polls = forms.ModelMultipleChoiceField(
        Poll.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple('Poll', False),
        required=False,
        help_text='Связанные опросы'
    )

    def __init__(self, *args, **kwargs):
        super(HistoryForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['polls'] = self.instance.polls.values_list('pk', flat=True)

    def save(self, commit=True):
        self.instance.date_assigned = timezone.now()
        self.instance.save()
        # TODO: розсилати тільки якщо щось змінювалося в групах або окремих користувачах
        users = self.instance.get_all_related_users()
        for user in users:
            try:
                UserHistory.objects.get(poll=self.instance, user=user)
            except ObjectDoesNotExist:
                user_history = UserHistory(poll=self.instance,
                                           user=user,
                                           date_created=timezone.now())
                user_history.save()

        # перевіряємо опитування
        # https://www.lasolution.be/blog/related-manytomanyfield-django-admin-site.html
        if self.instance.pk:
            for poll in self.instance.polls.all():
                if poll not in self.cleaned_data['polls']:
                    # we remove polls which have been unselected
                    self.instance.polls.remove(poll)
            for poll in self.cleaned_data['polls']:
                if poll not in self.instance.polls.all():
                    # we add newly selected polls
                    self.instance.polls.add(poll)

        return super(HistoryForm, self).save(commit=commit)

    class Meta:
        fields = '__all__'
        model = PollHistory


class HistoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_assigned']
    fieldsets = [
        (None, {'fields': ['name', 'groups', 'separate_users', 'text', 'polls', 'date_assigned']}),
        ('Связанные', {'fields': ['related_groups', 'related_separate_users', 'related_polls']}),
    ]
    filter_horizontal = ['groups', ]
    readonly_fields = ('date_assigned', 'related_groups', 'related_separate_users', 'related_polls')
    form = HistoryForm

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'groups':
            kwargs['queryset'] = UserFilter.objects.order_by('name')
        return super(HistoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def related_groups(self, obj):
        string = ''
        for gh in obj.groups.all().order_by('name'):
            try:
                string += '<a href="{0}">{1}</a>, {2}<br>'.format(
                    reverse("admin:users_userfilter_change", args=(gh.pk,)),
                    gh.name, UserHistory.objects.filter(user__pk=gh.users.first().pk, poll__pk=obj.pk)[0].date_created)
            except Exception as e:
                logger.exception("Failed to display related group: ", gh.name)
                pass
                # дата присвоєння історії групі визначається за датою присвоєння першому її члену
                # окрему таблицю GroupHistory вирішив не робити через мороку з формами
        return mark_safe(string)

    related_groups.short_description = 'Группы, которым отправлялась история'

    def related_separate_users(self, obj):
        string = ''
        for uh in obj.userhistory_set.filter(user__pk__in=obj.separate_users.values_list('pk')):
            string += '<a href="{0}">{1}</a>, {2}<br>'.format(
                reverse("admin:users_userprofile_change", args=(uh.user.pk,)),
                uh.user.user.username, uh.date_created)
        return mark_safe(string)

    related_separate_users.short_description = 'Отдельные пользователи'

    def related_polls(self, obj):
        string = ''
        for poll in obj.polls.all():
            string += '<a href="{0}">{1}</a><br>'.format(
                reverse("admin:polls_poll_change", args=(poll.pk,)),
                poll.name)
        return mark_safe(string)

    related_polls.short_description = 'Связанные опросы'


class HistoryTranslatedAdmin(HistoryAdmin, TranslationAdmin):
    pass


class UserHistoryAdmin(admin.ModelAdmin):
    model = UserHistory
    search_fields = ['user__user__username']
    list_filter = ['poll']


class NewsAdmin(TranslationAdmin):
    """ deprecated """
    list_display = ('text', 'date')


admin_site.register(PollHistory, HistoryTranslatedAdmin)
admin_site.register(UserHistory, UserHistoryAdmin)
# admin_site.register(News, NewsAdmin)
