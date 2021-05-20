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


class AnswerSerializer(serializers.ModelSerializer, MyHelper):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())

    class Meta:
        model = Answer
        fields = ['question', 'answer']

    def create(self, validated_data):
        my_helper = MyHelper()
        try:
            quiz = my_helper.get_active_quiz_by_pk(self.context['quiz'])
            user = my_helper.get_create_user(self.context['user'])
            my_helper.check_question_by_quiz(validated_data['question'], quiz)
            my_helper.check_answer_by_question(validated_data['question'], validated_data['answer'])
        except ValidationError as e:
            raise ValidationError(e.detail[0], code=400)

        answer = Answer(
            answer=validated_data['answer'],
            question=validated_data['question'],
            quiz=quiz,
            user_id=user
        )
        answer.save()
        return answer

