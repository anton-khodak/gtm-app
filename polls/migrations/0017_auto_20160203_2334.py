# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-03 21:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0016_auto_20160131_1435'),
    ]

    operations = [
        migrations.CreateModel(
            name='PollAdditional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intro', models.TextField(blank=True, max_length=2500, null=True, verbose_name='Вступительный текст')),
                ('outro', models.TextField(blank=True, max_length=3000, null=True, verbose_name='Заключительный текст')),
            ],
        ),
        migrations.AddField(
            model_name='poll',
            name='additional',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.PollAdditional', verbose_name='Дополнительно'),
        ),
    ]
