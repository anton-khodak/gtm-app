from django.db import models
from django.utils import timezone
from constants.constants import *
from constants.helpers import unique_chain
from constants.models import *
from history.models import PollHistory
from medicine.models import Medicine
from users.models import UserProfile, UserFilter
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from itertools import chain


class PollAdditional(models.Model):
    intro = models.TextField('Вступительный текст', max_length=2500, null=True, blank=True)
    outro = models.TextField('Заключительный текст', max_length=3000, null=True, blank=True)

    def __str__(self):
        return str(self.intro[:40]) + str(self.outro[:40])


class Poll(models.Model):
    name = models.CharField('Название опроса', max_length=150)
    users = models.ManyToManyField(UserProfile, through='UsersPoll')
    score = models.IntegerField('Баллов за опрос', default=0)
    poll_type = models.CharField('Тип опроса', choices=POLL_CHOICES, default=POLL_CHOICES[0][0], max_length=10)
    user_group = models.ManyToManyField(UserFilter, verbose_name='Для какой группы назначен опрос', blank=True)
    separate_users = models.ManyToManyField(UserProfile, verbose_name='Отдельные пользователи',
                                            related_name='separate_user', blank=True)
    histories = models.ManyToManyField(PollHistory, verbose_name='Связанные истории', blank=True, related_name='polls')
    medicine = models.ForeignKey(Medicine, verbose_name='Лекарство', default=None, null=True, blank=True, on_delete=models.SET_NULL)
    additional = models.ForeignKey(PollAdditional, verbose_name='Дополнительно', default=None, null=True, blank=True, on_delete=models.SET_NULL)
    change_date = models.DateTimeField('Дата последнего изменения опроса', default=timezone.now)

    def __str__(self):
        return self.name

    def get_all_related_users(self):
        users = UserProfile.objects.none()
        user_groups = self.user_group.all()
        if user_groups:
            for user_group in user_groups:
                new_users = user_group.get_filtered_user_queryset()
                users = list(unique_chain(users, new_users))
        separate_users = self.separate_users.all()
        if separate_users:
            users = list(unique_chain(users, separate_users))
        return users

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
        return ' / '.join((str(self.user), str(self.poll), str(self.passed)))


class Question(models.Model):
    text = models.TextField('Текст перед вопросом', max_length=7550, blank=True)
    question_text = models.TextField('Текст вопроса', max_length=2000, blank=True)
    poll = models.ForeignKey(Poll, verbose_name='К какому опросу принадлежит вопрос', null=True, blank=True,
                             related_name='questions', on_delete=models.SET_NULL)
    level = models.ForeignKey('Poll', related_name='lev')
    user_answers = models.ManyToManyField(UserProfile, through='UserAnswer')

    def __str__(self):
        if self.question_text:
            return self.question_text[:60]
        else:
            return self.text[:60]

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
                                 blank=True, on_delete=models.SET_NULL)
    next_question = models.ForeignKey(Question,
                                      related_name='next',
                                      verbose_name='Следующий вопрос',
                                      null=True,
                                      blank=True, on_delete=models.SET_NULL)
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
    date_answered = models.DateTimeField('Дата ответа', default=timezone.now, null=True)

    class Meta:
        unique_together = ['user', 'question']

    def __str__(self):
        return ' / '.join((str(self.user), str(self.question), str(self.answer)))


class UserPollFilter(models.Model):
    name = models.CharField(max_length=100, blank=True)
    group = models.ForeignKey(UserFilter, verbose_name='Группа пользователей', null=True, blank=True, on_delete=models.SET_NULL)
    date_from = models.DateField('Дата прохождения от', null=True, blank=True)
    date_to = models.DateField('Дата прохождения до', null=True, blank=True)
    polls = models.ManyToManyField(Poll, verbose_name='Конкретные опросы', blank=True)
    users = models.ManyToManyField(UserProfile, verbose_name='Конкретные пользователи', blank=True)
    order = models.CharField('Групировка', choices=ORDER_CHOICES, default=ORDER_CHOICES[0][0], max_length=25)

    def get_filtered_user_queryset(self):
        if self.group:
            qs = self.group.get_filtered_user_queryset()
        else:
            qs = None
        if qs:
            qs = list(unique_chain(qs, UserProfile.objects.filter(user__in=self.users.all())))
            qs = UserProfile.objects.filter(pk__in=[u.pk for u in qs])
        elif self.users:
            qs = UserProfile.objects.filter(user__in=self.users.all())
        else:
            qs = UserProfile.objects.all()
        return qs

    def __str__(self):
        if self.name:
            return self.name
        for order_choices in ORDER_CHOICES:
            if order_choices[0] == self.order:
                order = order_choices[1]
        return ' '.join((str(self.group), str(order)))


@receiver(m2m_changed, sender=Poll.user_group.through)
def delete_old_userpolls(sender, instance, action, *args, **kwargs):
    try:
        user_groups = Poll.objects.get(pk=instance.pk).user_group.all()
    except ObjectDoesNotExist:
        user_groups = []
    users = []
    if action == 'pre_remove':
        for user_group in user_groups:
            new_users = user_group.get_filtered_user_queryset()
            users = chain(users, new_users)
        users = list(users)
        UsersPoll.objects.filter(poll=instance, user__in=users).delete()

# @receiver(m2m_changed, sender=Poll.separate_users.through)
# def delete_old_userpolls(sender, instance, action, *args, **kwargs):
#     try:
#         user_groups = Poll.objects.get(pk=instance.pk).user_group.all()
#     except ObjectDoesNotExist:
#         user_groups = []
#     users = []
#     if action == 'pre_remove':
#         for user_group in user_groups:
#             new_users = user_group.get_filtered_user_queryset()
#             users = chain(users, new_users)
#         users = list(users)
#         UsersPoll.objects.filter(poll=instance, user__in=users).delete()

# TODO: delete_old_userspolls for separate users


# @receiver(m2m_changed, sender=Poll.histories.through)
# def send_histories_to_users_from_related_polls(sender, instance, action, reverse, pk_set, *args, **kwargs):
#     # if poll modified in history.admin
#     if reverse:
#         polls = Poll.objects
#     # if history modified in poll.admin
#     else:
#         try:
#             histories = PollHistory.objects.get(pk=instance.pk).groups.all()
#         except ObjectDoesNotExist:
#             histories = []
#     users = []
#     if action == 'pre_remove':
#         if isinstance(instance, Poll):
#             histories = PollHistory.objects.all()
#         for user_group in user_groups:
#             new_users = user_group.get_filtered_user_queryset()
#             users = chain(users, new_users)
#         users = list(users)
#     elif action == 'pre_add':
#         pass