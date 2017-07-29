# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-24 23:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20170423_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpollfilter',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.UserFilter', verbose_name='Группа пользователей'),
        ),
    ]
