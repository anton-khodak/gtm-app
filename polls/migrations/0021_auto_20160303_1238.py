# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-03 12:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0020_auto_20160229_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='name_ru',
            field=models.CharField(max_length=40, null=True, verbose_name='Название опроса'),
        ),
        migrations.AddField(
            model_name='poll',
            name='name_ua',
            field=models.CharField(max_length=40, null=True, verbose_name='Название опроса'),
        ),
    ]
