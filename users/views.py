import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.request import QueryDict
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import View, TemplateView
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from users.models import UserProfile
from users.serializers import UserSerializer, UserExchangeHistorySerializer, UserSessionSerializer


class UserView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)

    def update(self, request, *args, **kwargs):
        user = UserProfile.objects.get(user=self.request.user)
        poll_score = int(request.data['score'])
        request.data['score'] = poll_score + user.score
        user.total_score += poll_score
        user.save()
        return super(UserView, self).update(request, *args, **kwargs)


class UserExchangeView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserExchangeHistorySerializer

    def create(self, request, *args, **kwargs):
        if type(request.data) is QueryDict:
            request.data._mutable = True
        request.data['user'] = request.user
        desired_exchange = int(request.data['exchange'])
        usr = UserProfile.objects.get(pk=request.user)
        if desired_exchange > usr.score:
            return Response(data='User tries to exchange more scores than he has',
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        elif desired_exchange < 1:
            return Response(data='Negative or zero values not allowed', status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            usr.score = usr.score - desired_exchange
            usr.total_exchange += desired_exchange
            usr.save(update_fields=['score', 'total_exchange'])

        return super(UserExchangeView, self).create(request, *args, **kwargs)


class UserSessionView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSessionSerializer

    def create(self, request, *args, **kwargs):
        if type(request.data) is QueryDict:
            request.data._mutable = True
        request.data['user'] = request.user
        # desired_exchange = int(request.data['exchange'])
        # request.data['time'] = datetime.datetime.now()
        usr = UserProfile.objects.get(pk=request.user)
        usr.user.last_login = datetime.datetime.now()
        # usr.save(update_fields=['last_login'])
        usr.save()
        return super(UserSessionView, self).create(request, *args, **kwargs)


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"
    login_url = "/login/"


class ExchangeView(View):
    template_name = "exchange.html"

    def get(self, request):
        user = UserProfile.objects.get(user=request.user)
        context = {'score': user.score}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        view = UserExchangeView.as_view()
        return view(request, *args, **kwargs)


class ContactView(TemplateView):
    template_name = "contact.html"


class AboutView(TemplateView):
    template_name = "about.html"


class AgreementView(TemplateView):
    template_name = "agreement.html"


class MainPageView(ListView):
    template_name = "company.html"

    def get_queryset(self):
        from history.models import News
        return News.objects.all()


class GTMView(View):
    template_name = "gtm.html"

    def get(self, request):
        user = UserProfile.objects.get(user=request.user)
        from history.models import News
        context = {'score': user.score, 'news': News.objects.all().order_by('-id')}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        view = UserExchangeView.as_view()
        return view(request, *args, **kwargs)
