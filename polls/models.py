from django.db import models
from django.utils import timezone
from constants.constants import *
from constants.models import *
from medicine.models import Medicine
from users.models import UserProfile, UserFilter


class PollAdditional(models.Model):
    intro = models.TextField('Вступительный текст', max_length=2500, null=True, blank=True)
    outro = models.TextField('Заключительный текст', max_length=3000, null=True, blank=True)

    def __str__(self):
        return str(self.intro[:40]) + str(self.outro[:40])


class Poll(models.Model):
    name = models.CharField('Название опроса', max_length=40)
    users = models.ManyToManyField(UserProfile, through='UsersPoll')
    score = models.IntegerField('Баллов за опрос', default=0)
    poll_type = models.CharField('Тип опроса', choices=POLL_CHOICES, default=POLL_CHOICES[0][0], max_length=10)
    user_group = models.ForeignKey(UserFilter, verbose_name='Для какой группы назначен опрос', default=None, null=True,
                                   blank=True)
    medicine = models.ForeignKey(Medicine, verbose_name='Лекарство', default=None, null=True, blank=True)
    additional = models.ForeignKey(PollAdditional, verbose_name='Дополнительно', default=None, null=True, blank=True)

    def __str__(self):
        return self.name


class UsersPoll(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='Пользователь')
    poll = models.ForeignKey(Poll, related_name='smth', verbose_name='Опрос')
    date_assigned = models.DateTimeField('Дата получения', default=timezone.now)
    date_passed = models.DateTimeField('Дата прохождения', default=timezone.now)
    passed = models.BooleanField('Пройдено', default=False)
    notification_sent = models.BooleanField('Оповещение отправлено', default=False)

    class Meta:
        unique_together = ['user', 'poll']

    def __str__(self):
        return str(self.user) + ' / ' + str(self.poll) + ' / ' + str(self.passed)


class Question(models.Model):
    text = models.TextField('Текст перед вопросом', max_length=7550, blank=True)
    question_text = models.TextField('Текст вопроса', max_length=850)
    poll = models.ForeignKey(Poll, verbose_name='К какому опросу принадлежит вопрос', null=True, blank=True,
                             related_name='questions')
    level = models.ForeignKey('Poll', related_name='lev')
    user_answers = models.ManyToManyField(UserProfile, through='UserAnswer')

    def __str__(self):
        return self.question_text[:60]

    def save(self, *args, **kwargs):
        self.poll = self.level
        super(Question, self).save(*args, **kwargs)

    class Meta:
        ordering = ('id',)


class Answer(models.Model):
    answer_text = models.CharField('Вариант ответа',
                                   max_length=450, )
    question = models.ForeignKey(Question,
                                 related_name='answers',
                                 verbose_name='К какому вопросу принадлежит этот ответ',
                                 null=True,
                                 blank=True)
    next_question = models.ForeignKey(Question,
                                      related_name='next',
                                      verbose_name='Следующий вопрос',
                                      null=True,
                                      blank=True)
    level = models.ForeignKey('Question',
                              related_name='lev')

    def __str__(self):
        return self.answer_text[:60]

    def save(self, *args, **kwargs):
        self.question = self.level
        super(Answer, self).save(*args, **kwargs)


class UserAnswer(models.Model):
    question = models.ForeignKey(Question)
    user = models.ForeignKey(UserProfile, null=True)
    answer = models.ForeignKey(Answer, verbose_name='Стандартный ответ: ', blank=True, null=True)
    other_answer = models.CharField('Ответ пользователя: ', max_length=40, blank=True)

    class Meta:
        unique_together = ['user', 'question']

    def __str__(self):
        return str(self.user) + ' / ' + str(self.question) + ' / ' + str(self.answer)


class UserPollFilter(models.Model):
    group = models.ForeignKey(UserFilter, verbose_name='Группа пользователей', null=True, default='')
    date_from = models.DateField('Дата прохождения от', null=True, blank=True)
    date_to = models.DateField('Дата прохождения до', null=True, blank=True)
    polls = models.ManyToManyField(Poll, verbose_name='Конкретные опросы', null=True, blank=True)
    users = models.ManyToManyField(UserProfile, verbose_name='Конкретные пользователи', null=True, blank=True)
    order = models.CharField('Групировка', choices=ORDER_CHOICES, default=ORDER_CHOICES[0][0], max_length=25)

    def get_filtered_user_queryset(self):
        qs = self.group.get_filtered_user_queryset()
        if qs:
            qs |= UserProfile.objects.filter(user__in=self.users.all())
        elif self.users:
            qs = UserProfile.objects.filter(user__in=self.users.all())
        else:
            qs = UserProfile.objects.all()
        return qs

    def __str__(self):
        for order_choices in ORDER_CHOICES:
            if order_choices[0] == self.order:
                order = order_choices[1]
        return str(self.group) + ' ' + str(order)
