from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import LANGUAGE_SESSION_KEY
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
        l = UsersPoll.objects.filter(user__user=self.request.user) \
            .order_by('-date_assigned')
        print(l)
        return l


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
        print(self.data['passed'])
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
        except ObjectDoesNotExist:
            raise Http404

        if 'poll_element' in kwargs:
            poll_element = kwargs['poll_element']
            # Якщо є початкове питання - рендеринг або тексту, або самого початкового питання
            if start_question:
                context = PollView.get_question_context(self, start_question, poll_element, users_poll)
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
                    users_poll_obj.passed = True
                    users_poll_obj.date_passed = timezone.now()
                    users_poll_obj.save()

                    context = {'text': final,
                               'button': 'Вернуться в главное меню',
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
                                   'button': 'Перейти к анализу',
                                   'button_name': 'proceed-text'}
                    # Якщо нема початкового, нема відповідей і запит на питання - це перше питання
                    elif poll_element == 'question':
                        context = PollView.get_question_context(self, initial_question, 'question', users_poll)
                    # Якщо запит на перший текст або на інтро, коли інтро немає
                    else:
                        context = PollView.get_question_context(self, initial_question, 'text', users_poll)
        # Якщо посилання без вказання елементу, перехід зі списку
        else:
            if start_question:
                return HttpResponseRedirect('text/' + str(start_question) + '/')
            else:
                return HttpResponseRedirect('intro/')
        context['title'] = users_poll_obj.poll.name
        if context.get('text', ''):
            context['text'] = context['text'].replace('{{', '<img width="100%" src="').replace('}}', '">')
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
                                                                       answer=Answer.objects.get(pk=answer),
                                                                       other_answer=own_answer,
                                                                       question=Question.objects.get(
                                                                           pk=int(question_id)))
            user_answer.save()
            next_question = Answer.objects.get(pk=answer).next_question
            if next_question:
                return HttpResponseRedirect('/polls/' + poll_id + '/text/' + str(next_question.id) + '/')
            else:
                return HttpResponseRedirect('/polls/' + poll_id + '/final/')
        elif 'proceed-text' in post:
            return HttpResponseRedirect('/polls/' + poll_id + '/text/' + question_id + '/')
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

    # @staticmethod
    def get_question_context(self, _question, poll_element, users_poll):
        question = users_poll.get_question_by_id(_question)
        if question['text'] and poll_element == 'text':
            context = {'text': question['text'], 'button': 'Опрос', 'button_name': 'proceed-question'}
        else:
            context = {'question': question['question_text'],
                       'answers': question['answers'],
                       'button': 'Подтвердить',
                       'button_name': 'proceed-text',}
        return context

    def get_object(self):
        return Medicine.objects.all()
