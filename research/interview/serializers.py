from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from .my_helper import MyHelper
from .models import *



class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = ['id', 'type']


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ['id', 'name']


class QuizSerializer(serializers.ModelSerializer, MyHelper):
    questions = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all(), required=False)
    class Meta:
        model = Quiz
        fields = ['id', 'name', 'start_date', 'end_date', 'active', 'description', 'questions']
        extra_kwargs = {
            'name': {'required': False},
            'end_date': {'required': False},
            'active': {'required': False},
            'start_date': {'required': False},
            'description': {'required': False},
            'questions': {'required': False}

        }

    def create(self, validated_data):
        if 'start_date' not in validated_data:
            raise ValidationError('start_date is mandatory for creating Quiz', code=status.HTTP_400_BAD_REQUEST)

        name = self.is_parameter_transfer(validated_data.get('name', None))
        active = validated_data.get('active', False)
        questions = validated_data.get('questions', [])

        quiz = Quiz(
            name=name,
            start_date=validated_data['start_date'],
            active=active,
            end_date=validated_data.get('end_date', None),
            description=validated_data.get('description', None)
        )
        quiz.save()
        quiz.questions.set(questions)
        quiz.save()
        return quiz

    def update(self, instance, validated_data):
        if 'start_date' in validated_data:
            raise ValidationError('You can\'t change start_date after creating Quiz', code=status.HTTP_400_BAD_REQUEST)

        instance.name = validated_data.get('name', instance.name)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.active = validated_data.get('active', instance.active)
        instance.description = validated_data.get('description', instance.description)
        instance.questions.set(validated_data.get('questions', instance.questions.all()))
        instance.save()
        return instance


class QuestionSerializer(serializers.ModelSerializer, MyHelper):
    type = QuestionTypeSerializer(required=False)
    question_option = QuestionOptionSerializer(required=False, many=True)
    quiz = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=Quiz.objects.all())

    class Meta:
        model = Question
        fields = ['id', 'name', 'type', 'question_option', 'quiz']
        extra_kwargs = {'name':  {'required': False}}

    def create(self, validated_data):
        name = self.is_parameter_transfer(validated_data.get('name', None))
        quiz = validated_data.get('quiz', [])
        q_type = self.get_create_q_type(validated_data.get('type', {'type': ''}))
        q_type, q_option = self.check_relation_q_type_q_option(q_type, validated_data.get('question_option', []))

        new_question_option = list(map(
            self.get_create_question_option,
            q_option
        ))

        new_question = Question(
            name=name,
            type=q_type
        )
        new_question.save()
        new_question.question_option.set(new_question_option)
        new_question.quiz.set(quiz)
        new_question.save()

        return new_question

    def update(self, instance, validated_data):
        q_type = validated_data.get('type', instance.type)
        q_option = validated_data.get('question_option', instance.question_option)
        q_type = self.get_create_q_type(q_type)
        q_type, q_option = self.check_relation_q_type_q_option(q_type, q_option)
        new_question_option = list(map(
            self.get_create_question_option,
            q_option
        ))

        instance.name = validated_data.get('name', instance.name)
        instance.type = q_type
        instance.question_option.set(new_question_option)
        instance.quiz.set(validated_data.get('quiz', instance.quiz.all()))
        instance.save()
        return instance


class AvailableQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'name', 'description']


class AnswerSerializer(serializers.ModelSerializer, MyHelper):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())

    class Meta:
        model = Answer
        fields = ['answer', 'question']



class PassedQuizSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    class Meta:
        model = Quiz
        fields = ['id', 'name', 'answers']


class QuestionForPassQuizSerializer(serializers.ModelSerializer):
    type = QuestionTypeSerializer()
    question_option = QuestionOptionSerializer(many=True)
    class Meta:
        model = Question
        fields = ['id', 'name', 'type', 'question_option']


class AnswerToQuizSerializer(serializers.ModelSerializer):
    questions = QuestionForPassQuizSerializer(many=True, required=False)

    class Meta:
        model = Quiz
        fields = ['questions']



