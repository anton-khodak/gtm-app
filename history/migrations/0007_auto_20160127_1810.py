# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-27 16:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0006_auto_20160110_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pollhistory',
            name='date_assigned',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 27, 18, 10, 27, 548829), verbose_name='Дата создания'),
        ),
    ]