# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-31 14:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20170330_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='user_group',
            field=models.ManyToManyField(blank=True, to='users.UserFilter', verbose_name='Для какой группы назначен опрос'),
        ),
    ]
