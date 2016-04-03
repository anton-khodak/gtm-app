from django.contrib.auth.models import User
from django.test import TestCase

from constants.models import *
from users.models import UserProfile


def create_user_filter():
    pass

def create_user():
    return User.objects.create_user(first_name="Вася", last_name="Пупкин", password="123", username="vasia")
    # k = UserManager()
    # return k.create_user('vasia')
def create_user_profile():
    city = City.objects.create(name="Киев")
    area = Area.objects.create(name="Киевская")
    # patronimyc = models.CharField('Отчество', max_length=17)
    # gender = models.CharField('Пол',
    #                           max_length=8,
    #                           choices=GENDER_CHOICES_USER_PROFILE,
    #                           default=EMPTY)
    # work = models.ForeignKey(Hospital, verbose_name='Место работы', default=EMPTY)
    curing_form = models.ForeignKey(CuringForm, verbose_name='Форма лечения', default=1)
    position = models.ForeignKey(Position, verbose_name='Должность', default=1, related_name='+', )
    category = models.ForeignKey(Category, verbose_name='Категория', default=1)
    speciality = Speciality.objects.create(name="Гинеколог")

    return UserProfile.objects.create(user=create_user(), city=city, gender="male", patronimyc="Иванович",
                                      speciality=speciality,
                                      district="Деснянский", house="22")


class UserViewTest(TestCase):
    def test_updates_user_agreement(self):
        user = create_user_profile()
        print(user)
        print(User.objects.all())
        self.client.login(username="vasia", password="123")
        response = self.client.put('/api/user/', data={'user_agreed': "True"})
        print(response.data)
        self.assertEqual(user.user_agreed, True)

