# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-02 13:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20170502_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfilter',
            name='area',
            field=models.ManyToManyField(blank=True, to='constants.Area', verbose_name='Область'),
        ),
        migrations.AlterField(
            model_name='userfilter',
            name='city',
            field=models.ManyToManyField(blank=True, to='constants.City', verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='userfilter',
            name='curing_form',
            field=models.ManyToManyField(blank=True, to='constants.CuringForm', verbose_name='Форма лечения'),
        ),
        migrations.AlterField(
            model_name='userfilter',
            name='speciality',
            field=models.ManyToManyField(blank=True, to='constants.Speciality', verbose_name='Специальность'),
        ),
        migrations.AlterField(
            model_name='userfilter',
            name='work',
            field=models.ManyToManyField(blank=True, to='constants.Hospital', verbose_name='Место работы'),
        ),
    ]
