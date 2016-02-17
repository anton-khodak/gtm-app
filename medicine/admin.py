from django.contrib import admin

from users.admin import admin_site
from medicine.models import *

class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    # fields = ['score', 'name', 'text']

# class MedicineAdmin(admin.ModelAdmin):


admin_site.register(SearchHistory, SearchHistoryAdmin)
admin_site.register(Medicine)