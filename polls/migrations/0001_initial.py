# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-30 15:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '__first__'),
        ('medicine', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(max_length=450, verbose_name='Вариант ответа')),
                ('answer_text_ru', models.CharField(max_length=450, null=True, verbose_name='Вариант ответа')),
                ('answer_text_uk', models.CharField(max_length=450, null=True, verbose_name='Вариант ответа')),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Название опроса')),
                ('name_ru', models.CharField(max_length=80, null=True, verbose_name='Название опроса')),
                ('name_uk', models.CharField(max_length=80, null=True, verbose_name='Название опроса')),
                ('score', models.IntegerField(default=0, verbose_name='Баллов за опрос')),
                ('poll_type', models.CharField(choices=[('simple', 'Простой'), ('text', 'Текстовый')], default='simple', max_length=10, verbose_name='Тип опроса')),
            ],
        ),
        migrations.CreateModel(
            name='PollAdditional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intro', models.TextField(blank=True, max_length=2500, null=True, verbose_name='Вступительный текст')),
                ('outro', models.TextField(blank=True, max_length=3000, null=True, verbose_name='Заключительный текст')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, max_length=7550, verbose_name='Текст перед вопросом')),
                ('text_ru', models.TextField(blank=True, max_length=7550, null=True, verbose_name='Текст перед вопросом')),
                ('text_uk', models.TextField(blank=True, max_length=7550, null=True, verbose_name='Текст перед вопросом')),
                ('question_text', models.TextField(blank=True, max_length=2000, verbose_name='Текст вопроса')),
                ('question_text_ru', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Текст вопроса')),
                ('question_text_uk', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Текст вопроса')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lev', to='polls.Poll')),
                ('poll', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='questions', to='polls.Poll', verbose_name='К какому опросу принадлежит вопрос')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('other_answer', models.CharField(blank=True, max_length=40, verbose_name='Ответ пользователя: ')),
                ('answer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.Answer', verbose_name='Стандартный ответ: ')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Question')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='UserPollFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField(blank=True, null=True, verbose_name='Дата прохождения от')),
                ('date_to', models.DateField(blank=True, null=True, verbose_name='Дата прохождения до')),
                ('order', models.CharField(choices=[('question__poll__id', 'По опросам'), ('user__user__id', 'По пользователям')], default='question__poll__id', max_length=25, verbose_name='Групировка')),
                ('group', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='users.UserFilter', verbose_name='Группа пользователей')),
                ('polls', models.ManyToManyField(blank=True, null=True, to='polls.Poll', verbose_name='Конкретные опросы')),
                ('users', models.ManyToManyField(blank=True, null=True, to='users.UserProfile', verbose_name='Конкретные пользователи')),
            ],
        ),
        migrations.CreateModel(
            name='UsersPoll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_assigned', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата получения')),
                ('date_passed', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата прохождения')),
                ('passed', models.BooleanField(default=False, verbose_name='Пройдено')),
                ('notification_sent', models.BooleanField(default=False, verbose_name='Оповещение отправлено')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='smth', to='polls.Poll', verbose_name='Опрос')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserProfile', verbose_name='Пользователь')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='user_answers',
            field=models.ManyToManyField(through='polls.UserAnswer', to='users.UserProfile'),
        ),
        migrations.AddField(
            model_name='poll',
            name='additional',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='polls.PollAdditional', verbose_name='Дополнительно'),
        ),
        migrations.AddField(
            model_name='poll',
            name='medicine',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='medicine.Medicine', verbose_name='Лекарство'),
        ),
        migrations.AddField(
            model_name='poll',
            name='user_group',
            field=models.ForeignKey(blank=True, default=' ', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='old_groups', to='users.UserFilter', verbose_name='Для какой группы назначен опрос'),
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
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next', to='polls.Question', verbose_name='Следующий вопрос'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='answers', to='polls.Question', verbose_name='К какому вопросу принадлежит этот ответ'),
        ),
        migrations.AlterUniqueTogether(
            name='userspoll',
            unique_together=set([('user', 'poll')]),
        ),
        migrations.AlterUniqueTogether(
            name='useranswer',
            unique_together=set([('user', 'question')]),
        ),
    ]
