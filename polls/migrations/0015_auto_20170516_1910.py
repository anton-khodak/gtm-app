# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-16 19:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_poll_histories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='histories',
            field=models.ManyToManyField(blank=True, related_name='polls', to='history.PollHistory', verbose_name='Связанные истории'),
        ),
    ]
