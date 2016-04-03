import django
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from constants.constants import *
from constants.models import *
from multiselectfield import MultiSelectField
import datetime


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='Пользователь')
    patronimyc = models.CharField('Отчество', max_length=17)
    gender = models.CharField('Пол',
                              max_length=8,
                              choices=GENDER_CHOICES_USER_PROFILE,
                              default=EMPTY)
    work = models.ForeignKey(Hospital, verbose_name='Место работы', default=EMPTY)
    curing_form = models.ForeignKey(CuringForm, verbose_name='Форма лечения', default=1)
    position = models.ForeignKey(Position, verbose_name='Должность', default=1, related_name='+', )
    category = models.ForeignKey(Category, verbose_name='Категория', default=1)
    speciality = models.ForeignKey(Speciality, verbose_name='Специальность', default=EMPTY)
    area = models.ForeignKey(Area, verbose_name='Область', default=EMPTY)
    city = models.ForeignKey(City, verbose_name='Город', default=EMPTY)

    age = models.IntegerField('Возраст', default=0)
    date_of_birth = models.DateField('Дата рождения', default=datetime.date(1970, 1, 1))
    main_phone = models.CharField('Моб. телефон 1', max_length=13, blank=True)
    secondary_phone = models.CharField('Моб. телефон 2', max_length=13, blank=True)
    work_phone = models.CharField('Рабочий телефон', max_length=13, blank=True)
    bed_quantity = models.IntegerField('Кол-во койко-мест', default=0)
    patient_quantity = models.IntegerField('Кол-во пациентов в месяц', default=0)

    district = models.CharField('Район', max_length=20, default=EMPTY)
    house = models.CharField('Дом', max_length=5, default=EMPTY)
    flat = models.IntegerField('Квартира', default=0)
    index = models.IntegerField('Индекс', default=0)

    score = models.IntegerField('Баллы', default=0)
    total_score = models.IntegerField('Баллов за всё время', default=0)
    total_exchange = models.IntegerField('Баллов обменяно за всё время', default=0)
    user_agreed = models.BooleanField('Согласие пользователя', default=False)

    def __str__(self):
        return self.user.username

    def save(self, update_groups=False, *args, **kwargs):
        if not update_groups:
            return super(UserProfile, self).save(*args, **kwargs)
        if self.work_phone and len(self.work_phone) < 7:
            self.work_phone = City.objects.get(name=self.city).phone_prefix + self.work_phone
        super(UserProfile, self).save(*args, **kwargs)
        user_groups = UserFilter.objects.all()
        for group in user_groups:
            print("Group: ", group)
            if self in group.get_filtered_user_queryset():
                group.users.add(self)
                group.save()

                from polls.models import Poll, UsersPoll
                polls = Poll.objects.filter(user_group=group)
                for poll in polls:
                    try:
                        UsersPoll.objects.get(poll=poll, user=self)
                    except ObjectDoesNotExist:
                        UsersPoll.objects.create(poll=poll,
                                                 user=self,
                                                 date_assigned=timezone.now(),
                                                 date_passed=timezone.now(),
                                                 passed=False)

                from history.models import PollHistory, UserHistory
                for history in PollHistory.objects.filter(user_group=group):
                    try:
                        UserHistory.objects.get(poll=history, user=self)
                    except ObjectDoesNotExist:
                        UserHistory.objects.create(poll=history,
                                                   user=self)

        return super(UserProfile, self).save(*args, **kwargs)


class UserFilter(models.Model):
    name = models.CharField('Название группы', max_length=30)
    gender = MultiSelectField('Пол',
                              max_length=16,
                              choices=GENDER_CHOICES,
                              blank=True)
    work = models.ManyToManyField(Hospital, verbose_name='Место работы', default=EMPTY, blank=True)
    curing_form = models.ManyToManyField(CuringForm, verbose_name='Форма лечения', default=None, blank=True)
    position = models.ManyToManyField(Position, verbose_name='Должность', default=None, blank=True)
    category = models.ManyToManyField(Category, verbose_name='Специальность', default=None, blank=True)
    speciality = models.ManyToManyField(Speciality, verbose_name='Специальность', default=EMPTY, blank=True)
    area = models.ManyToManyField(Area, verbose_name='Область', default=EMPTY, blank=True)
    city = models.ManyToManyField(City, verbose_name='Город', default=EMPTY, blank=True)
    age_from = models.IntegerField('Возраст от', blank=True, null=True)
    age_to = models.IntegerField('Возраст до', blank=True, null=True)
    bed_quantity_from = models.IntegerField('Кол-во койко-мест от', blank=True, null=True)
    bed_quantity_to = models.IntegerField('Кол-во койко-мест до', blank=True, null=True)
    patient_quantity_from = models.IntegerField('Кол-во пациентов в месяц от', blank=True, null=True)
    patient_quantity_to = models.IntegerField('Кол-во пациентов в месяц до', blank=True, null=True)

    users = models.ManyToManyField(UserProfile, verbose_name='Пользователи в группе', null=True, blank=True)

    def get_filtered_user_queryset(self):
        q = UserProfile.objects.all()
        if self.gender:
            genders = self.gender
            if len(genders) < len(GENDER_CHOICES):
                q = q.filter(gender=genders[0])

        many_to_many_fields = ['curing_form', 'category', 'work', 'position', 'speciality', 'area', 'city']
        for field in many_to_many_fields:
            value = getattr(self, field)
            if value:
                objects = getattr(self, field).all()
                q_objects = Q()
                for obj in objects:
                    q_objects |= Q(**{field: obj})
                print(q_objects)
                print(q)
                q = q.filter(q_objects)
                print(q)

        from_fields = ['age_from', 'bed_quantity_from', 'patient_quantity_from']
        to_fields = ['age_to', 'bed_quantity_to', 'patient_quantity_to']

        for field in from_fields:
            value = getattr(self, field)
            if value:
                q = q.filter(**{field.replace('_from', '') + '__gte': value})

        for field in to_fields:
            value = getattr(self, field)
            if value:
                q = q.filter(**{field.replace('_to', '') + '__lte': value})
        return q

    def save(self, *args, **kwargs):
        super(UserFilter, self).save(*args, **kwargs)  # Call the "real" save() method.
        print(self.users)
        self.users = self.get_filtered_user_queryset()
        print(self.users)
        return super(UserFilter, self).save(*args, **kwargs)  # Call the "real" save() method.

    def __str__(self):
        return self.name


class UserExchangeHistory(models.Model):
    user = models.ForeignKey(UserProfile)
    exchange = models.IntegerField('Сколько пользователь захотел обменять баллов', default=0)
    date = models.DateTimeField('Дата обмена', default=timezone.now)

    def __str__(self):
        return str(self.user) + ' обменял ' + str(self.exchange) + ' баллов, ' + str(self.date)


class UserSession(models.Model):
    user = models.ForeignKey(UserProfile)
    duration = models.DurationField(verbose_name='Длительность сеанса')
    time = models.DateTimeField(verbose_name='Время сеанса', default=timezone.now)

    def __str__(self):
        return str(self.user.user.username) + ' / ' + str(self.time) + ' / ' + str(self.duration)
