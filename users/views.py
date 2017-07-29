import datetime

from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.http.request import QueryDict
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import View, TemplateView
from push_notifications.api.rest_framework import GCMDeviceAuthorizedViewSet, APNSDeviceAuthorizedViewSet
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin

from users.models import UserProfile
from users.serializers import UserSerializer, UserExchangeHistorySerializer, UserSessionSerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class UserView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = UserSerializer

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)

    def update(self, request, *args, **kwargs):
        agreement = request.data['user_agreed']
        if agreement:
            user = UserProfile.objects.get(user=self.request.user)
            user.user_agreed = eval(agreement)
            user.save(update_fields=("user_agreed",))
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
        usr = UserProfile.objects.get(pk=request.user)
        now = datetime.datetime.now()
        last_login = usr.user.last_login
        usr.user.last_login = now
        usr.user.save()
        if request.data.get('browser', ''):
            k = (now - last_login).seconds
            if (now - last_login).seconds < 60*3:
                raise Exception
        return super(UserSessionView, self).create(request, *args, **kwargs)


class AgreementRequiredMixin(AccessMixin):
    """
    CBV mixin which verifies that the current user agreed with user agreement.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return self.handle_no_permission(destination=self.login_url)
        try:
            user = UserProfile.objects.get(user=request.user)
            if not user.user_agreed:
                return self.handle_no_permission(destination=self.agreement_url)
        except:
            pass
        return super(AgreementRequiredMixin, self).dispatch(request, *args, **kwargs)

    def handle_no_permission(self, destination):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect_to_login(self.request.get_full_path(), destination, self.get_redirect_field_name())


class HomeView(AgreementRequiredMixin, TemplateView):
    template_name = "home.html"
    login_url = "/login/"
    agreement_url = "/agreement-start/"


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


class AgreementStartView(TemplateView):
    template_name = "agreement_start.html"


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


class GCMDeviceAuthorizedViewSetWithLogging(LoggingMixin, GCMDeviceAuthorizedViewSet):
    logging_methods = ['POST']


class APNSDeviceAuthorizedViewSetWithLogging(LoggingMixin, APNSDeviceAuthorizedViewSet):
    logging_methods = ['POST']