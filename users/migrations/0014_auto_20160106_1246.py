# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-06 10:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20160106_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 6, 12, 46, 4, 166788), verbose_name='Дата обмена'),
        ),
    ]