# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-30 16:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_remove_poll_user_group'),
    ]

    operations = [
        migrations.RenameField(
            model_name='poll',
            old_name='user_groups',
            new_name='user_group',
        ),
    ]