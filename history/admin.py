from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from users.admin import admin_site
from history.models import *


class HistoryForm(forms.ModelForm):
    def save(self, commit=True):
        self.instance.save()
        user_group = self.instance.user_group
        if user_group:
            users = user_group.get_filtered_user_queryset()
        else:
            users = UserProfile.objects.all()
        for user in users:
            try:
                UserHistory.objects.get(poll=self.instance, user=user)
            except ObjectDoesNotExist:
                userspoll = UserHistory(poll=self.instance,
                                        user=user)
                userspoll.save()
                print(userspoll)
        return super(HistoryForm, self).save(commit=commit)

    class Meta:
        fields = '__all__'
        model = PollHistory


class HistoryAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    fields = ['name', 'user_group', 'text']
    form = HistoryForm


admin_site.register(PollHistory, HistoryAdmin)
admin_site.register(UserHistory)