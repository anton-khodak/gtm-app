from rest_framework import serializers
from history.models import *


class PollHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = PollHistory
        fields = ('id', 'name', 'date_assigned', 'text')


class UserPollHistorySerializer(serializers.ModelSerializer):
    poll = PollHistorySerializer(read_only=True)

    class Meta:
        model = UserHistory
        fields = ('user', 'poll',)