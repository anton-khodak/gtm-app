# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-06 10:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20160106_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='user_group',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='users.UserFilter', verbose_name='Для какой группы назначен опрос'),
        ),
    ]
