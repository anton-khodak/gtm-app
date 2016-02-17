# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-04 22:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(max_length=100, verbose_name='Вариант ответа')),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Название опроса')),
                ('score', models.IntegerField(default=0, verbose_name='Баллов за опрос')),
                ('poll_type', models.CharField(choices=[('simple', 'Простой'), ('text', 'Текстовый')], default='simple', max_length=10, verbose_name='Тип опроса: ')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, max_length=450, verbose_name='Текст перед вопросом')),
                ('question_text', models.CharField(max_length=200, verbose_name='Текст вопроса')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lev', to='polls.Poll')),
                ('poll', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='polls.Poll', verbose_name='К какому опросу принадлежит вопрос')),
            ],
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('other_answer', models.CharField(blank=True, max_length=40, verbose_name='Ответ пользователя: ')),
                ('answer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.Answer', verbose_name='Стандартный ответ: ')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='UsersPoll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_assigned', models.DateTimeField(default=datetime.datetime.now, verbose_name='Дата получения')),
                ('date_passed', models.DateTimeField(default=datetime.datetime.now, verbose_name='Дата прохождения')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='smth', to='polls.Poll')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='user_answers',
            field=models.ManyToManyField(through='polls.UserAnswer', to='users.UserProfile'),
        ),
        migrations.AddField(
            model_name='poll',
            name='users',
            field=models.ManyToManyField(through='polls.UsersPoll', to='users.UserProfile'),
        ),
        migrations.AddField(
            model_name='answer',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lev', to='polls.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='next_question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next', to='polls.Question', verbose_name='Следующий вопрос'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='polls.Question', verbose_name='К какому вопросу принадлежит этот ответ'),
        ),
    ]
