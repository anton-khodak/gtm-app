# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-23 20:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_userpollfilter_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Название опроса'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='name_ru',
            field=models.CharField(max_length=150, null=True, verbose_name='Название опроса'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='name_uk',
            field=models.CharField(max_length=150, null=True, verbose_name='Название опроса'),
        ),
    ]