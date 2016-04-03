from django.db import models


class City(models.Model):
    name = models.CharField('Название города', max_length=20)
    phone_prefix = models.CharField('Код телефона', max_length=5, blank=True)

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField('Название области', max_length=20)

    def __str__(self):
        return self.name


class Speciality(models.Model):
    name = models.CharField('Название специальности', max_length=20)

    def __str__(self):
        return self.name


class Hospital(models.Model):
    name = models.CharField('Название лечебного учреждения', max_length=100)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField('Название должности', max_length=30)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField('Название района', max_length=20)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Название категории', max_length=30)

    def __str__(self):
        return self.name


class CuringForm(models.Model):
    name = models.CharField('Название формы лечения', max_length=30)

    def __str__(self):
        return self.name
