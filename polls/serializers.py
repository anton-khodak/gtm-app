from rest_framework import serializers

from medicine.serializers import MedicineFullSerializer
from polls.models import *
from django.contrib.auth.models import User


class AnswerSerializer(serializers.ModelSerializer):
    next_question = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'answer_text', 'next_question']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'question_text', 'answers')
        ordering = ('id',)


class AdditionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollAdditional
        fields = ('intro', 'outro')


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    medicine = MedicineFullSerializer()
    additional = AdditionalSerializer()

    class Meta:
        model = Poll
        fields = ('id', 'name', 'poll_type', 'score', 'medicine', 'additional', 'questions')


class UsersPollSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.username')
    poll = PollSerializer(read_only=True)
    start_question = serializers.SerializerMethodField()

    @staticmethod
    def get_start_question(obj):
        answers = UserAnswer.objects.filter(question__poll=obj.poll, user__user=obj.user)
        if answers:
            answer = max(answers, key=lambda a: a.question_id)
            if answer.answer.next_question:
                return answer.answer.next_question.id

    def get_question_by_id(self, id):
        for i, question in enumerate(self.data['poll']['questions']):
            if question['id'] == id:
                return question

    class Meta:
        model = UsersPoll
        fields = ('user', 'date_assigned', 'poll', 'start_question')


class UsersPollFullSerializer(UsersPollSerializer):

    class Meta:
        model = UsersPoll
        fields = ('user', 'date_assigned', 'date_passed', 'poll',)



class UsersPollUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersPoll
        fields = ('user', 'poll', 'date_passed', 'passed')
        read_only_fields = ('user', 'poll')


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'