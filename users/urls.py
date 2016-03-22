from django.conf.urls import url
from push_notifications.api.rest_framework import GCMDeviceAuthorizedViewSet, APNSDeviceAuthorizedViewSet
from rest_framework.urlpatterns import format_suffix_patterns
from users.views import *

urlpatterns = [
    url('^$', MainPageView.as_view()),
    url(r'^api/user/$', UserView.as_view()),
    url(r'^api/user/exchange/$', UserExchangeView.as_view()),
    url(r'^api/user/duration/$', UserSessionView.as_view()),
    url(r'^home/$', HomeView.as_view()),
    url(r'^exchange/$', ExchangeView.as_view()),
    url(r'^contact/$', ContactView.as_view()),
    url(r'^about/$', AboutView.as_view()),
    url(r'^gtm/$', GTMView.as_view()),
    url(r'^agreement/$', AgreementView.as_view()),
    url(r'^device/android/$', GCMDeviceAuthorizedViewSet.as_view({'post': 'create'})),
    url(r'^device/ios/$', APNSDeviceAuthorizedViewSet.as_view({'post': 'create'})),

]

urlpatterns = format_suffix_patterns(urlpatterns)