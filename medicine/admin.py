from daterange_filter.filter import DateRangeFilter
from django.contrib import admin
from django_pandas.io import read_frame

from constants.excel import export_to_xls
from constants.helper_functions import translate_column_names
from users.admin import admin_site
from medicine.models import *


class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    list_filter = [('date', DateRangeFilter), 'user']
    actions = ['export_to_xls_search_history']

    def export_to_xls_search_history(self, request, queryset):
        df = read_frame(queryset,
                        verbose=True,
                        fieldnames=(
                            'user__user__id', 'user__user__username',
                            'date',
                            'name',
                        ))
        df = translate_column_names(df)
        return export_to_xls(df,
                             'search_history' +
                             request.GET.get('drf__day__gte ', '') +
                             request.GET.get('drf__day__lte', '') + '.xls',
                             engine='openpyxl')

    export_to_xls_search_history.short_description = 'Выгрузить информацию об истории поисков в xls'


admin_site.register(SearchHistory, SearchHistoryAdmin)
admin_site.register(Medicine)
