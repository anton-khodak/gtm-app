from rest_framework import serializers
from medicine.models import *


class SearchHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SearchHistory

class MedicineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medicine
        fields = ('name',)

class MedicineFullSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medicine
        fields = ('name', 'instruction')