# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-04 22:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_auto_20160105_0038'),
    ]

    operations = [
        migrations.CreateModel(
            name='PollHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Краткое название')),
                ('text', models.TextField(max_length=200, verbose_name='Краткое содержание')),
                ('score', models.IntegerField(default=0, verbose_name='Баллов за опрос')),
                ('date_assigned', models.DateTimeField(default=datetime.datetime(2016, 1, 5, 0, 38, 17, 924495), verbose_name='Дата создания')),
            ],
        ),
        migrations.CreateModel(
            name='UserHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='history.PollHistory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='pollhistory',
            name='users',
            field=models.ManyToManyField(through='history.UserHistory', to='users.UserProfile'),
        ),
    ]
