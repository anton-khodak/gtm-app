"""Arthur URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from ajax_select import urls as ajax_select_urls
from debug_toolbar import urls as debug_toolbar_urls
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from rest_framework.urlpatterns import format_suffix_patterns

from polls.admin import admin_site
from polls.views import UsersPollList

urlpatterns = [
    url(r'^admin/', include(admin_site.urls)),
    url(r'^', include('rest_framework.urls',
                      namespace='rest_framework')),
    url(r'', include('users.urls', namespace='users')),
    url(r'', include('medicine.urls', namespace='medicine')),
    url(r'', include('polls.urls', namespace='polls')),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^__debug__/', include(debug_toolbar_urls)),
    url(r'^ajax_select/', include(ajax_select_urls)),
]

poll_patern = format_suffix_patterns([
    url(r'^$', UsersPollList.as_view()),
])


urlpatterns += i18n_patterns(

    url(r'', include('history.urls', namespace='history')),
    url(r'api/polls', include(poll_patern)),
        url(r'', include('users.urls', namespace='users')),
    url(r'', include('medicine.urls', namespace='medicine')),
    url(r'', include('polls.urls', namespace='polls')),

)


