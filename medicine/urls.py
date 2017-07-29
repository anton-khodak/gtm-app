from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from medicine.views import *

urlpatterns = [
    url(r'^api/search-history/$', UserSearchHistoryList.as_view()),
    url(r'^api/medicine/$', MedicineList.as_view()),
    url(r'medicine-autocomplete/$', MedicineAutocomplete.as_view(), name='/medicine-autocomplete/',),
    url(r'medicine-search/$', MedicineSearchView.as_view(), name='/medicine-search/',),
]

urlpatterns = format_suffix_patterns(urlpatterns)