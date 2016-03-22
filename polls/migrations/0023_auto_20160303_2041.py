# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-03 20:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0022_auto_20160303_2036'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_text_ru',
            field=models.TextField(max_length=850, null=True, verbose_name='Текст вопроса'),
        ),
        migrations.AddField(
            model_name='question',
            name='question_text_uk',
            field=models.TextField(max_length=850, null=True, verbose_name='Текст вопроса'),
        ),
        migrations.AddField(
            model_name='question',
            name='text_ru',
            field=models.TextField(blank=True, max_length=7550, null=True, verbose_name='Текст перед вопросом'),
        ),
        migrations.AddField(
            model_name='question',
            name='text_uk',
            field=models.TextField(blank=True, max_length=7550, null=True, verbose_name='Текст перед вопросом'),
        ),
    ]
