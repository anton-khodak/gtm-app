# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-14 14:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_auto_20160214_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 14, 16, 27, 17, 659267), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='day',
            field=models.DateField(default=datetime.date(2016, 2, 14), verbose_name='Дата обмена'),
        ),
    ]
