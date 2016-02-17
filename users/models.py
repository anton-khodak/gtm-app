import django
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
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
    curing_form = models.CharField('Форма лечения',
                                   max_length=15,
                                   choices=CURING_FORM_CHOICES_USER_PROFILE,
                                   default=EMPTY, )
    position = models.ForeignKey(Position, verbose_name='Должность', default=EMPTY, related_name='+', )
    category = models.CharField('Категория', choices=CATEGORY_CHOICES_USER_PROFILE, default=EMPTY, max_length=15)
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

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.work_phone and len(self.work_phone) < 7:
            self.work_phone = City.objects.get(name=self.city).phone_prefix + self.work_phone
        return super(UserProfile, self).save(*args, **kwargs)


class UserFilter(models.Model):
    name = models.CharField('Название группы', max_length=30)
    gender = MultiSelectField('Пол',
                              max_length=16,
                              choices=GENDER_CHOICES,
                              blank=True)
    work = models.ManyToManyField(Hospital, verbose_name='Место работы', default=EMPTY, blank=True)
    curing_form = MultiSelectField('Форма лечения',
                                   max_length=34,
                                   choices=CURING_FORM_CHOICES,
                                   blank=True)
    position = models.ManyToManyField(Position, verbose_name='Должность', default=EMPTY, related_name='+', blank=True)
    category = MultiSelectField('Категория', choices=CATEGORY_CHOICES, default=EMPTY, max_length=34, blank=True)
    speciality = models.ManyToManyField(Speciality, verbose_name='Специальность', default=EMPTY, blank=True)
    area = models.ManyToManyField(Area, verbose_name='Область', default=EMPTY, blank=True)
    city = models.ManyToManyField(City, verbose_name='Город', default=EMPTY, blank=True)
    age_from = models.IntegerField('Возраст от', blank=True, null=True)
    age_to = models.IntegerField('Возраст до', blank=True, null=True)
    bed_quantity_from = models.IntegerField('Кол-во койко-мест от', blank=True, null=True)
    bed_quantity_to = models.IntegerField('Кол-во койко-мест до', blank=True, null=True)
    patient_quantity_from = models.IntegerField('Кол-во пациентов в месяц от', blank=True, null=True)
    patient_quantity_to = models.IntegerField('Кол-во пациентов в месяц до', blank=True, null=True)

    def get_filtered_user_queryset(self):
        print(self)
        q = UserProfile.objects.all()
        if self.gender:
            genders = self.gender
            if len(genders) < len(GENDER_CHOICES):
                q = q.filter(gender=genders[0])

        if self.curing_form:
            curing_forms = self.curing_form
            if len(curing_forms) < len(CURING_FORM_CHOICES):
                q = q.filter(curing_form=curing_forms[0])
        if self.category:
            field = 'category'
            if getattr(self, field):
                # переписати пізніше з DRY
                objects = getattr(self, field)
                q_objects = Q()
                for obj in objects:
                    q_objects |= Q(**{field: obj})
                q = q.filter(q_objects)

        many_to_many_fields = ['work', 'position', 'speciality', 'area', 'city']
        for field in many_to_many_fields:
            if getattr(self, field):
                objects = getattr(self, field).all()
                q_objects = Q()
                for obj in objects:
                    q_objects |= Q(**{field: obj})
                q = q.filter(q_objects)

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

    def __str__(self):
        return self.name


class UserExchangeHistory(models.Model):
    user = models.ForeignKey(UserProfile)
    exchange = models.IntegerField('Сколько пользователь захотел обменять баллов', default=0)
    date = models.DateTimeField('Дата обмена', default=datetime.datetime.now())
    # day = models.DateField('Дата обмена', default=django.utils.timezone.now())
    day = models.DateField('Дата обмена', default=datetime.date.today())

    def __str__(self):
        return str(self.user) + ' обменял ' + str(self.exchange) + ' баллов, ' + str(self.date)
