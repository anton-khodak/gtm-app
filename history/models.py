import datetime

from django.db import models
from users.models import UserProfile, UserFilter


class PollHistory(models.Model):
    name = models.CharField('Краткое название', max_length=40)
    text = models.TextField('Краткое содержание', max_length=2300)
    date_assigned = models.DateTimeField('Дата создания', default=datetime.datetime.now())
    users = models.ManyToManyField(UserProfile, through='UserHistory')
    user_group = models.ForeignKey(UserFilter, verbose_name='Какой группе пользователей отправить текст', default=None,
                                   null=True, blank=True)

    def __str__(self):
        return self.name


class UserHistory(models.Model):
    user = models.ForeignKey(UserProfile)
    poll = models.ForeignKey(PollHistory)

    def __str__(self):
        return str(self.user) + ' / ' + str(self.poll)
