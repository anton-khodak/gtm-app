# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-06 10:05
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20160106_1152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='exchange_score',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='total_exchange',
            field=models.IntegerField(default=0, verbose_name='Баллов обменяно за всё время'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 6, 12, 5, 0, 586222), verbose_name='Дата обмена'),
        ),
    ]
