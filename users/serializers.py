from rest_framework import serializers
from users.models import *


class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='user.id')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    username = serializers.ReadOnlyField(source='user.username')
    city = serializers.ReadOnlyField(source='city.name')

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'first_name', 'last_name', 'patronimyc', 'gender', 'city', 'score')

    def update(self, instance, validated_data):
        instance = super(UserSerializer, self).update(instance, validated_data)
        return instance


class UserExchangeHistorySerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    score = serializers.ReadOnlyField(source='user.score')

    class Meta:
        model = UserExchangeHistory
        fields = ['user', 'username', 'score', 'exchange', 'date', 'id']


class UserSessionSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserSession
        fields = ['user', 'username', 'duration', 'time']