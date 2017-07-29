import datetime
from itertools import chain

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils import timezone

from constants.helpers import unique_chain
from users.models import UserProfile, UserFilter


class PollHistory(models.Model):
    name = models.CharField('Краткое название', max_length=100)
    text = models.TextField('Краткое содержание')
    date_assigned = models.DateTimeField('Дата последнего изменения', default=timezone.now)
    users = models.ManyToManyField(UserProfile, through='UserHistory')
    separate_users = models.ManyToManyField(UserProfile, verbose_name='Отдельные пользователи',
                                            related_name='separate_user_history', blank=True)
    # deprecated field
    user_group = models.ForeignKey(UserFilter, verbose_name='Какой группе пользователей отправить текст', default=None,
                                   null=True, blank=True)
    groups = models.ManyToManyField(UserFilter, verbose_name='Группа', related_name='groups', blank=True)

    def get_all_related_users(self):
        users = UserProfile.objects.none()
        user_groups = self.groups.all()
        if user_groups:
            for user_group in user_groups:
                new_users = user_group.get_filtered_user_queryset()
                users = list(unique_chain(users, new_users))
        separate_users = self.separate_users.all()
        if separate_users:
            users = list(unique_chain(users, separate_users))
        return users

    def __str__(self):
        return self.name


class UserHistory(models.Model):
    user = models.ForeignKey(UserProfile)
    poll = models.ForeignKey(PollHistory)
    date_created = models.DateTimeField('Дата отправления', null=True)

    def __str__(self):
        return ' / '.join((str(self.user), str(self.poll)))


class News(models.Model):
    """ deprecated class """

    text = models.TextField('Текст новости')
    date = models.DateField('Дата создания', default=datetime.date.today)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.text[:100]


@receiver(m2m_changed, sender=PollHistory.users.through)
def delete_old_userhistories(sender, instance, action, *args, **kwargs):
    try:
        user_groups = PollHistory.objects.get(pk=instance.pk).groups.all()
    except ObjectDoesNotExist:
        user_groups = []
    users = []
    if action == 'pre_remove':
        for user_group in user_groups:
            new_users = user_group.get_filtered_user_queryset()
            users = chain(users, new_users)
        users = list(users)
        UserHistory.objects.filter(poll=instance, user__in=users).delete()