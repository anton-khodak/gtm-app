# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-15 19:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0010_auto_20170515_1851'),
        ('polls', '0013_useranswer_date_answered'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='histories',
            field=models.ManyToManyField(blank=True, to='history.PollHistory', verbose_name='Связанные истории'),
        ),
    ]
