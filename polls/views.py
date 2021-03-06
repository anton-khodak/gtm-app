from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.views.generic.list import ListView
from rest_framework import generics
from rest_framework import permissions

from polls.serializers import *


class UsersPollList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UsersPollSerializer

    def get(self, request, *args, **kwargs):
        # lang = request.GET.get('lang', 'ru')
        # request.session[LANGUAGE_SESSION_KEY] = lang
        return super(UsersPollList, self).get(self, request, *args, **kwargs)

    def get_queryset(self):
        return UsersPoll.objects.filter(user__user=self.request.user) \
            .filter(passed=False) \
            .order_by('-date_assigned')


class UsersPollFullList(UsersPollList):
    serializer_class = UsersPollFullSerializer

    def get_queryset(self):
        return UsersPoll.objects.filter(user__user=self.request.user).order_by('-date_assigned')


class UserAnswerList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserAnswerSerializer

    def create(self, request, *args, **kwargs):
        self.data = request.data.copy()
        user = request.user
        for item in self.data:
            item['user'] = user
        return super(UserAnswerList, self).create(self, *args, **kwargs)

    def get_queryset(self):
        return UserAnswer.objects.filter(user__user=self.request.user)

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]
            if isinstance(data, list):
                kwargs["many"] = True
        return super(UserAnswerList, self).get_serializer(*args, **kwargs)


class UserPollPassedView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UsersPollUpdateSerializer

    def update(self, request, *args, **kwargs):
        request = self.initialize_request(request)
        self.data = request.data.copy()
        self.data['date_passed'] = timezone.now()
        self.data['passed'] = True
        user = UserProfile.objects.get(user=self.request.user)
        poll_score = Poll.objects.get(pk=int(request.data['poll'])).score
        user.score += poll_score
        user.total_score += poll_score
        user.save()
        return super(UserPollPassedView, self).update(self, *args, **kwargs)

    def get_object(self):
        return UsersPoll.objects.get(user__user=self.request.user, poll=self.data['poll'])


class PollsList(ListView):
    template_name = 'polls.html'

    def get_queryset(self):
        return UsersPoll.objects.filter(user__user=self.request.user) \
            .filter(passed=False) \
            .filter(poll__poll_type='simple') \
            .order_by('-date_assigned')


class TextPollsList(PollsList):
    def get_queryset(self):
        return UsersPoll.objects.filter(user__user=self.request.user) \
            .filter(passed=False) \
            .filter(poll__poll_type='text') \
            .order_by('-date_assigned')


class PollView(View):
    template_name = 'poll.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        poll_id = kwargs['poll_id']
        try:
            users_poll_obj = UsersPoll.objects.get(user__user=user, poll=poll_id)
            users_poll = UsersPollSerializer(users_poll_obj)
            start_question = UsersPollSerializer.get_start_question(users_poll_obj)
            initial_question = users_poll.data['poll']['questions'][0]['id']
            current_question = kwargs.get('question_id', '')
            if current_question:
                current_question = int(current_question)
        except ObjectDoesNotExist:
            raise Http404

        if 'poll_element' in kwargs:
            poll_element = kwargs['poll_element']
            # Якщо є початкове питання - рендеринг або тексту, або самого початкового питання
            if start_question:
                if kwargs.get('question_id', ''):
                    if (poll_element == 'atext'):
                        # users_poll.get_question_by_id(int(kwargs['question_id']))['question_text']:
                        start_question = current_question
                        poll_element = 'text'
            if start_question:
                if current_question and current_question > start_question:
                    start_question = current_question
                context = PollView.get_question_context(start_question, poll_element, users_poll)
            else:
                answers = UserAnswer.objects.filter(question__poll=poll_id, user__user=user)
                # Якщо є відповіді, але нема початкового питання - це фінальний текст
                if answers:
                    try:
                        final = users_poll.data['poll']['additional']['outro']
                    except TypeError:
                        final = None
                        pass
                    try:
                        instruction = users_poll.data['poll']['medicine']['instruction']
                    except TypeError:
                        instruction = None
                        pass
                    try:
                        medicine = users_poll.data['poll']['medicine']['name']
                        city = UserProfile.objects.get(pk=user).city.name
                        link = "http://google.com/search?q=" + medicine + "+" + str(city).replace(" ", "+") + "+купить"
                    except TypeError:
                        medicine = city = link = None
                        pass
                    if not users_poll_obj.passed:
                        users_poll_obj.passed = True
                        users_poll_obj.date_passed = timezone.now()
                        user = UserProfile.objects.get(user=user)
                        poll_score = int(users_poll.data['poll']['score'])
                        user.score += poll_score
                        user.total_score += poll_score
                        user.save()
                        users_poll_obj.save()

                    context = {'text': final,
                               'button': _('Вернуться в главное меню'),
                               'instruction': instruction,
                               'medicine': medicine,
                               'city': city,
                               'link': link,
                               'button_name': 'main-menu'}
                else:
                    additional = users_poll.data['poll']['additional']
                    # Якщо нема відповідей і запит на "інтро" - інтро
                    if additional and poll_element == 'intro':
                        context = {'text': additional['intro'],
                                   'button': _('Перейти к анализу'),
                                   'button_name': 'proceed-text'}
                    # Якщо нема початкового, нема відповідей і запит на питання - це перше питання
                    elif poll_element == 'question':
                        context = PollView.get_question_context(initial_question, 'question', users_poll)

                    # Якщо запит на перший текст або на інтро, коли інтро немає
                    else:
                        context = PollView.get_question_context(initial_question, 'text', users_poll)
        # Якщо посилання без вказання елементу, перехід зі списку
        else:
            if start_question:
                return HttpResponseRedirect('text/' + str(start_question) + '/')
            else:
                return HttpResponseRedirect('intro/')
        context['title'] = users_poll_obj.poll.name
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        post = request.POST.copy()
        poll_id = kwargs['poll_id']
        try:
            users_poll_obj = UsersPoll.objects.get(user__user=request.user, poll=poll_id)
            users_poll = UsersPollSerializer(users_poll_obj)
            initial_question = users_poll.data['poll']['questions'][0]['id']
        except ObjectDoesNotExist:
            raise Http404
        question_id = kwargs.get('question_id', str(initial_question))
        if 'answer' in post:
            answer = int(post['choice'])
            own_answer = post.get('user-answer', '')
            user_answer, created = UserAnswer.objects.update_or_create(user=UserProfile.objects.get(user=request.user),
                                                                       question=Question.objects.get(pk=int(question_id)),
                                                                       defaults={
                                                                           'answer': Answer.objects.get(pk=answer),
                                                                           'other_answer': own_answer,
                                                                       })
            user_answer.save()
            next_question = Answer.objects.get(pk=answer).next_question
            if next_question:
                return HttpResponseRedirect('/polls/' + poll_id + '/text/' + str(next_question.id) + '/')
            else:
                return HttpResponseRedirect('/polls/' + poll_id + '/final/')
        elif 'proceed-final' in post:
            return HttpResponseRedirect('/polls/' + poll_id + '/final/')
        elif 'proceed-text' in post:
            return HttpResponseRedirect('/polls/' + poll_id + '/text/' + question_id + '/')
        elif 'proceed-text-without-question' in post:
            question_id = Answer.objects.get(question__id=int(kwargs['question_id'])).next_question.id
            return HttpResponseRedirect('/polls/' + poll_id + '/atext/' + str(question_id))
        elif 'proceed-question' in post:
            return HttpResponseRedirect('/polls/' + poll_id + '/question/' + question_id + '/')
        elif 'instruction' in post:
            try:
                instruction = users_poll.data['poll']['medicine']['instruction']
                medicine = users_poll.data['poll']['medicine']['name']
            except TypeError:
                instruction = None
                medicine = None
            context = {'name': medicine, 'text': instruction}
            return render(request, "history.html", context)
        elif 'main-menu' in post:
            return HttpResponseRedirect('/home/')

    @staticmethod
    def get_question_context(_question, poll_element, users_poll):
        question = users_poll.get_question_by_id(_question)

        if question['text'] and poll_element == 'text':
            if question['question_text']:
                context = {'text': question['text'], 'button': _('Опрос'), 'button_name': 'proceed-question'}
            else:
                context = {'text': question['text'], 'button': _('Продолжить'), 'button_name': 'proceed-text-without-question'}
        else:
            context = {'question': question['question_text'],
                       'answers': question['answers'],
                       'button': _('Подтвердить'),
                       'button_name': 'proceed-text', }
            context['question'] = context['question']
        return context
