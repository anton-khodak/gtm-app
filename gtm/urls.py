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
from django.conf.urls import include, url
from django.contrib import admin
from polls.admin import admin_site

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    # url(r'^admin/', include(admin_site.site.urls)),
    url(r'^admin/', include(admin_site.urls)),
    url(r'^', include('rest_framework.urls',
                      namespace='rest_framework')),
    url(r'', include('polls.urls', namespace='polls')),
    url(r'', include('users.urls', namespace='users')),
    url(r'', include('history.urls', namespace='history')),
    url(r'', include('medicine.urls', namespace='medicine')),
    url(r'^nested_admin/', include('nested_admin.urls')),
]
