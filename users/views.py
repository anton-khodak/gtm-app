from django.http.request import QueryDict
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic.base import View, TemplateView
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from users.models import UserProfile
from users.serializers import UserSerializer, UserExchangeHistorySerializer


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


class HomeView(TemplateView):
    template_name = "home.html"


class ExchangeView(View):
    template_name = "exchange.html"

    def get(self, request):
        user = UserProfile.objects.get(user=request.user)
        context = {'score': user.score}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        view = UserExchangeView.as_view()
        return view(request, *args, **kwargs)