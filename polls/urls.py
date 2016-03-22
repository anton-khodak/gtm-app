from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from polls.views import *

urlpatterns = [
    # url(r'^api/polls/$', UsersPollList.as_view()),
    url(r'^api/polls/all/$', UsersPollFullList.as_view()),
    url(r'^api/polls/passed/$', UserPollPassedView.as_view()),
    url(r'^api/answers/$', UserAnswerList.as_view()),
    url(r'^text-polls/$', TextPollsList.as_view()),
    url(r'^polls/$', PollsList.as_view()),
    url(r'^polls/(?P<poll_id>[0-9]+)/$', PollView.as_view()),
    url(r'^polls/(?P<poll_id>[0-9]+)/(?P<poll_element>(\w)+)/$', PollView.as_view()),
    url(r'^polls/(?P<poll_id>[0-9]+)/(?P<poll_element>(\w)+)/(?P<question_id>[0-9]+)/$', PollView.as_view()),
    url(r'^text-polls/(?P<poll_id>[0-9]+)/$', PollView.as_view()),
    url(r'^text-polls/(?P<poll_id>[0-9]+)/(?P<poll_element>(\w)+)/$', PollView.as_view()),
    url(r'^text-polls/(?P<poll_id>[0-9]+)/(?P<poll_element>(\w)+)/(?P<question_id>[0-9]+)/$', PollView.as_view()),
    # url(r'^text-polls/(?P<question_id>[0-9]+)//$', TextPollView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)