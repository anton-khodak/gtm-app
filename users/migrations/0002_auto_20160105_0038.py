# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-04 22:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 5, 0, 38, 17, 912487), verbose_name='Дата обмена'),
        ),
    ]