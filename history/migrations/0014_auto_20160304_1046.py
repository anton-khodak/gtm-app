# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-04 10:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0013_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='text_ru',
            field=models.TextField(max_length=2000, null=True, verbose_name='Текст новости'),
        ),
        migrations.AddField(
            model_name='news',
            name='text_uk',
            field=models.TextField(max_length=2000, null=True, verbose_name='Текст новости'),
        ),
        migrations.AddField(
            model_name='pollhistory',
            name='name_ru',
            field=models.CharField(max_length=40, null=True, verbose_name='Краткое название'),
        ),
        migrations.AddField(
            model_name='pollhistory',
            name='name_uk',
            field=models.CharField(max_length=40, null=True, verbose_name='Краткое название'),
        ),
        migrations.AddField(
            model_name='pollhistory',
            name='text_ru',
            field=models.TextField(max_length=2300, null=True, verbose_name='Краткое содержание'),
        ),
        migrations.AddField(
            model_name='pollhistory',
            name='text_uk',
            field=models.TextField(max_length=2300, null=True, verbose_name='Краткое содержание'),
        ),
    ]
