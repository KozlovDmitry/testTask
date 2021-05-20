from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .my_helper import MyHelper
from .models import *


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


class QuizAdditionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        exclude = ['start_date']
        extra_kwargs = {
            'name': {'required': False},
            'description': {'required': False},
            'end_date': {'required': False}
        }


class QuestionSerializer(serializers.ModelSerializer):
    quiz = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all(), many=True)
    class Meta:
        model = Question
        fields = '__all__'


class QuestionAdditionalSerializer(serializers.ModelSerializer):
    quiz = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all(), many=True, required=False)

    class Meta:
        model = Question
        fields = '__all__'
        extra_kwargs = {
            'text': {'required': False},
            'type': {'required': False},
        }


class QuestionByQuizSerializer(serializers.ModelSerializer):
    question = QuestionAdditionalSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['question']


class MyCustomeSerializer(serializers.Serializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    answer = serializers.CharField()


class AnswerSerializer(serializers.ModelSerializer, MyHelper):
    user_id = serializers.IntegerField()
    quiz = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all())

    class Meta:
        model = Answer
        fields = ['user_id', 'quiz']

    def create(self, validated_data):
        quiz = self.get_active_quiz_by_pk(validated_data['quiz'].id)

        my_helper = MyHelper({
            'quiz': quiz,
            'user_id': self.get_create_user(validated_data['user_id'])
        })

        answers = list(map(
            my_helper.answer_creater,
            self.context['answers']
        ))

        raw_answer = Answer.objects.bulk_create(answers)
        return self.beauty_answer(raw_answer)
