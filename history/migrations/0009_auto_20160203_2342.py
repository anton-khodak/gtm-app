# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-03 21:42
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0008_auto_20160131_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pollhistory',
            name='date_assigned',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 3, 23, 42, 19, 637300), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='pollhistory',
            name='text',
            field=models.TextField(max_length=2300, verbose_name='Краткое содержание'),
        ),
    ]
