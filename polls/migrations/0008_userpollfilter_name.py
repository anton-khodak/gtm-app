# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-04 11:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_poll_change_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpollfilter',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
