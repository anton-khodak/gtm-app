# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-13 12:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_auto_20160131_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 13, 14, 10, 40, 288004), verbose_name='Дата обмена'),
        ),
    ]