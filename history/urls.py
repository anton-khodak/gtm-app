from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from history.views import *


urlpatterns = [
    url(r'^api/history/$', UserPollHistoryList.as_view()),
    url(r'^api/news/$', NewsList.as_view()),
    url(r'^history-search/$', HistorySearch.as_view()),
    url(r'^history/$', HistoryListView.as_view()),
    url(r'^news/$', NewsView.as_view()),
    url(r'^company/news/$', CompanyNewsView.as_view()),
    url(r'^company/medicine-news/$', MedicineNewsView.as_view()),
    url(r'^history/(?P<history_id>[0-9]+)/$', HistoryView.as_view()),
]



urlpatterns = format_suffix_patterns(urlpatterns)