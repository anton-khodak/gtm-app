import datetime

from django.db import models

from users.models import UserProfile
from constants.constants import *
from constants.models import *


class Medicine(models.Model):
    name = models.CharField('Название лекарства', max_length=40)
    instruction = models.TextField('Инструкция', max_length=20000, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class SearchHistory(models.Model):
    name = models.CharField('Название лекарства', max_length=40)
    date = models.DateTimeField('Дата создания', default=datetime.datetime.now())
    user = models.ForeignKey(UserProfile)

    def __str__(self):
        return self.name