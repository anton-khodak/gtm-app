from django.http import JsonResponse
from django.http.request import QueryDict
from django.shortcuts import render
from django.views.generic import View
from rest_framework import generics
from rest_framework import permissions

from medicine.serializers import *


class MedicineList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MedicineSerializer

    def get_queryset(self):
        return Medicine.objects.all()


class UserSearchHistoryList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SearchHistorySerializer

    def create(self, request, *args, **kwargs):
        if type(request.data) is QueryDict:
            request.data._mutable = True
            request.data['user'] = request.user
        else:
            data = request.data
            user = request.user
            for item in data:
                item['user'] = user
        return super(UserSearchHistoryList, self).create(request, *args, **kwargs)

    def get_queryset(self):
        return SearchHistory.objects.filter(user__user=self.request.user).order_by('-date')

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]

            if isinstance(data, list):
                kwargs["many"] = True

        return super(UserSearchHistoryList, self).get_serializer(*args, **kwargs)


class MedicineAutocomplete(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            q = request.GET.get('term', '')
            drugs = Medicine.objects.filter(name__icontains=q)[:20]
            results = []
            for drug in drugs:
                drug_json = {}
                drug_json['id'] = drug.id
                drug_json['label'] = drug.name
                drug_json['value'] = drug.name
                results.append(drug_json)
        else:
            results = 'fail'
        return JsonResponse(results, safe=False)


class MedicineSearchView(View):
    template_name = "medicine_search.html"

    def get(self, request):
        user = UserProfile.objects.get(pk=request.user.id)
        context = {'city': user.city.name.replace(" ", "+")}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        view = UserSearchHistoryList.as_view()
        return view(request, *args, **kwargs)

