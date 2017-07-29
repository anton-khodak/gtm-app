from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from rest_framework import generics
from rest_framework import permissions
from history.models import UserHistory, News
from history.serializers import UserPollHistorySerializer, NewsSerializer


class UserPollHistoryList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserPollHistorySerializer

    def get_queryset(self):
        return UserHistory.objects.filter(user__user=self.request.user) \
            .order_by('-poll__date_assigned')


class HistoryListView(ListView):
    template_name = 'history_list.html'

    def get_queryset(self):
        return UserHistory.objects.filter(user__user=self.request.user) \
            .order_by('-poll__date_assigned')


class HistoryView(View):
    template_name = 'history.html'

    def get(self, request, *args, **kwargs):
        history = UserHistory.objects.get(user__user=request.user, poll__id=kwargs['history_id'])
        context = {'name': history.poll.name,
                   'text': history.poll.text}
        return render(request, self.template_name, context)


class HistorySearch(ListView):
    template_name = 'content.html'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            self.user = request.user
            self.q = request.GET.get('q', '')
        return super(HistorySearch, self).get(request, *args, **kwargs)

    def get_queryset(self):
        q = self.q
        history = UserHistory.objects.filter(user__user=self.user)
        return history.filter(Q(poll__name__icontains=q) | Q(poll__text__contains=q)).order_by('-poll__date_assigned')


class NewsList(generics.ListAPIView):
    serializer_class = NewsSerializer
    queryset = News.objects.all().order_by('-date')


class NewsView(ListView):
    template_name = "news.html"
    queryset = News.objects.all()


class CompanyNewsView(NewsView):
    template_name = "company_news.html"


class MedicineNewsView(TemplateView):
    template_name = "medicine_news.html"
