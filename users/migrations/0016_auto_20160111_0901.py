# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-11 07:01
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20160110_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='patronimyc',
            field=models.CharField(default='Сильвестрович', max_length=17, verbose_name='Отчество'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 11, 9, 0, 23, 758782), verbose_name='Дата обмена'),
        ),
    ]