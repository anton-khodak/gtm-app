# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-10 19:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0004_auto_20160106_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pollhistory',
            name='date_assigned',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 21, 49, 19, 666669), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='pollhistory',
            name='text',
            field=models.TextField(max_length=300, verbose_name='Краткое содержание'),
        ),
    ]
