# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-02 13:06
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import multiselectfield.db.fields


class Migration(migrations.Migration):

    replaces = [('users', '0001_initial'), ('users', '0002_auto_20160105_0038'), ('users', '0003_auto_20160106_0051'), ('users', '0004_auto_20160106_0051'), ('users', '0005_auto_20160106_0052'), ('users', '0006_auto_20160106_0055'), ('users', '0007_auto_20160106_0058'), ('users', '0008_auto_20160106_0058'), ('users', '0009_auto_20160106_0911'), ('users', '0010_auto_20160106_0914'), ('users', '0011_auto_20160106_0948'), ('users', '0012_auto_20160106_1152'), ('users', '0013_auto_20160106_1205'), ('users', '0014_auto_20160106_1246'), ('users', '0015_auto_20160110_2149'), ('users', '0016_auto_20160111_0901'), ('users', '0017_auto_20160127_1810'), ('users', '0018_auto_20160131_1435'), ('users', '0019_auto_20160213_1410'), ('users', '0020_auto_20160213_1416'), ('users', '0021_auto_20160214_1440'), ('users', '0022_auto_20160214_1443'), ('users', '0023_auto_20160214_1627'), ('users', '0024_auto_20160214_1628'), ('users', '0025_auto_20160214_1630'), ('users', '0026_auto_20160214_1631'), ('users', '0027_auto_20160214_1633'), ('users', '0028_auto_20160215_1020'), ('users', '0029_auto_20160219_1327'), ('users', '0030_auto_20160219_1338'), ('users', '0031_auto_20160224_1427'), ('users', '0032_auto_20160229_1844'), ('users', '0033_userprofile_position'), ('users', '0034_userfilter_users'), ('users', '0035_auto_20160229_1958'), ('users', '0036_auto_20160229_2015'), ('users', '0037_userprofile_user_agreed'), ('users', '0038_auto_20160402_1302')]

    initial = True

    dependencies = [
        ('constants', '0004_category_curingform'),
        ('auth', '0007_alter_validators_add_error_messages'),
        ('constants', '__first__'),
        ('constants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserExchangeHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exchange', models.IntegerField(default=0, verbose_name='Сколько пользователь захотел обменять баллов')),
                ('date', models.DateTimeField(default=datetime.datetime(2016, 1, 5, 0, 35, 19, 926170), verbose_name='Дата обмена')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('gender', models.CharField(choices=[(' ', 'Выбрать...'), ('male', 'Мужчина'), ('female', 'Женщина')], default=' ', max_length=8, verbose_name='Пол')),
                ('curing_form', models.CharField(choices=[(' ', 'Выбрать...'), ('stationar', 'Cтационарное'), ('poliklinika', 'Поликлиническое')], default=' ', max_length=15, verbose_name='Форма лечения')),
                ('category', models.CharField(choices=[(' ', 'Выбрать...'), ('first', 'Первая'), ('second', 'Вторая'), ('no_category', 'Без категории')], default=' ', max_length=15, verbose_name='Категория')),
                ('age', models.IntegerField(default=0, verbose_name='Возраст')),
                ('date_of_birth', models.DateField(default=datetime.date(1970, 1, 1), verbose_name='Дата рождения')),
                ('main_phone', models.CharField(blank=True, max_length=13, verbose_name='Моб. телефон 1')),
                ('secondary_phone', models.CharField(blank=True, max_length=13, verbose_name='Моб. телефон 2')),
                ('work_phone', models.CharField(blank=True, max_length=13, verbose_name='Рабочий телефон')),
                ('bed_quantity', models.IntegerField(default=0, verbose_name='Кол-во койко-мест')),
                ('patient_quantity', models.IntegerField(default=0, verbose_name='Кол-во пациентов в месяц')),
                ('district', models.CharField(default=' ', max_length=20, verbose_name='Район')),
                ('house', models.CharField(default=' ', max_length=5, verbose_name='Дом')),
                ('flat', models.IntegerField(default=0, verbose_name='Квартира')),
                ('index', models.IntegerField(default=0, verbose_name='Индекс')),
                ('score', models.IntegerField(default=0, verbose_name='Баллы')),
                ('area', models.ForeignKey(default=' ', on_delete=django.db.models.deletion.CASCADE, to='constants.Area', verbose_name='Область')),
                ('city', models.ForeignKey(default=' ', on_delete=django.db.models.deletion.CASCADE, to='constants.City', verbose_name='Город')),
                ('speciality', models.ForeignKey(default=' ', on_delete=django.db.models.deletion.CASCADE, to='constants.Speciality', verbose_name='Специальность')),
                ('work', models.ForeignKey(default=' ', on_delete=django.db.models.deletion.CASCADE, to='constants.Hospital', verbose_name='Место работы')),
                ('total_score', models.IntegerField(default=0, verbose_name='Баллов за всё время')),
                ('total_exchange', models.IntegerField(default=0, verbose_name='Баллов обменяно за всё время')),
                ('patronimyc', models.CharField(default='Сильвестрович', max_length=17, verbose_name='Отчество')),
            ],
        ),
        migrations.AddField(
            model_name='userexchangehistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserProfile'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 5, 0, 38, 17, 912487), verbose_name='Дата обмена'),
        ),
        migrations.CreateModel(
            name='UserFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Название группы')),
                ('gender', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('male', 'Мужчина'), ('female', 'Женщина')], max_length=16, verbose_name='Пол')),
                ('curing_form', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('stationar', 'Cтационарное'), ('poliklinika', 'Поликлиническое')], max_length=34, verbose_name='Форма лечения')),
                ('category', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('first', 'Первая'), ('second', 'Вторая'), ('no_category', 'Без категории')], default=' ', max_length=34, verbose_name='Категория')),
                ('age_from', models.IntegerField(blank=True, null=True, verbose_name='Возраст от')),
                ('age_to', models.IntegerField(blank=True, null=True, verbose_name='Возраст до')),
                ('bed_quantity_from', models.IntegerField(blank=True, null=True, verbose_name='Кол-во койко-мест от')),
                ('bed_quantity_to', models.IntegerField(blank=True, null=True, verbose_name='Кол-во койко-мест до')),
                ('patient_quantity_from', models.IntegerField(blank=True, null=True, verbose_name='Кол-во пациентов в месяц от')),
                ('patient_quantity_to', models.IntegerField(blank=True, null=True, verbose_name='Кол-во пациентов в месяц до')),
                ('category', models.ManyToManyField(blank=True, default=None, to='constants.Category', verbose_name='Специальность')),
                ('curing_form', models.ManyToManyField(blank=True, default=None, to='constants.CuringForm', verbose_name='Форма лечения')),
            ],
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 6, 0, 51, 19, 559737), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 6, 0, 51, 58, 49839), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 6, 0, 52, 2, 969242), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 6, 0, 55, 37, 234489), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 6, 0, 58, 19, 557367), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 6, 0, 58, 24, 662281), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 6, 9, 11, 52, 112777), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 6, 9, 14, 8, 963298), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 6, 9, 48, 54, 239520), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 6, 11, 52, 43, 200258), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 6, 12, 5, 0, 586222), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 6, 12, 46, 4, 166788), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 21, 49, 19, 656661), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 11, 9, 0, 23, 758782), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 27, 18, 10, 27, 530817), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 31, 14, 35, 29, 896582), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 13, 14, 10, 40, 288004), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 13, 14, 16, 5, 546376), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 14, 14, 40, 34, 632918), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 14, 14, 43, 30, 215519), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 14, 16, 27, 17, 659267), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 14, 16, 28, 21, 430706), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 14, 16, 30, 8, 125398), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 14, 16, 31, 16, 199758), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 14, 16, 33, 38, 487955), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 15, 10, 20, 41, 942289), verbose_name='Дата обмена'),
        ),
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.DurationField(verbose_name='Длительность сеанса')),
                ('time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время сеанса')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserProfile')),
            ],
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 19, 13, 27, 57, 735319), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 19, 13, 38, 18, 196849), verbose_name='Дата обмена'),
        ),
        migrations.AlterField(
            model_name='userexchangehistory',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата обмена'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='constants.Category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='curing_form',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='constants.CuringForm', verbose_name='Форма лечения'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='position',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='constants.Position', verbose_name='Должность'),
        ),
        migrations.AddField(
            model_name='userfilter',
            name='users',
            field=models.ManyToManyField(blank=True, null=True, to='users.UserProfile', verbose_name='Пользователи в группе'),
        ),
        migrations.AddField(
            model_name='userfilter',
            name='area',
            field=models.ManyToManyField(blank=True, default=' ', to='constants.Area', verbose_name='Область'),
        ),
        migrations.AddField(
            model_name='userfilter',
            name='city',
            field=models.ManyToManyField(blank=True, default=' ', to='constants.City', verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='userfilter',
            name='position',
            field=models.ManyToManyField(blank=True, default=None, to='constants.Position', verbose_name='Должность'),
        ),
        migrations.AddField(
            model_name='userfilter',
            name='speciality',
            field=models.ManyToManyField(blank=True, default=' ', to='constants.Speciality', verbose_name='Специальность'),
        ),
        migrations.AddField(
            model_name='userfilter',
            name='work',
            field=models.ManyToManyField(blank=True, default=' ', to='constants.Hospital', verbose_name='Место работы'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_agreed',
            field=models.BooleanField(default=False, verbose_name='Согласие пользователя'),
        ),
    ]
