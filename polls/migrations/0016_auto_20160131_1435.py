# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-31 12:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0015_poll_medicine'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='useranswer',
            unique_together=set([('user', 'question')]),
        ),
    ]