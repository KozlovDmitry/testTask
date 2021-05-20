from rest_framework.exceptions import ValidationError
from .models import *
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import datetime
import pytz


class MyHelper:
    def __init__(self, context=None):
        self.context = context

    def get_active_quizs(self, default_tz='Europe/Moscow'):
        t = pytz.timezone(default_tz).localize(datetime.datetime.now())
        return Quiz.objects.filter(Q(start_date__lte=t) & Q(end_date__gte=t))

    def get_active_quiz_by_pk(self, pk, default_tz='Europe/Moscow'):
        t = pytz.timezone(default_tz).localize(datetime.datetime.now())

        try:
            quiz = Quiz.objects.get(
                Q(pk=pk)
                & Q(start_date__lte=t)
                & Q(end_date__gte=t)
            )
        except ObjectDoesNotExist:
            raise ValidationError('This quiz is not active', code=400)
        return quiz

    def get_create_user(self, user_id):
        if not isinstance(user_id, int):
            raise ValidationError('user_id must be integer', code=400)
        try:
            user = UserOfResearch.objects.get(user_id=user_id)
        except ObjectDoesNotExist:
            user = UserOfResearch(user_id=user_id)
            user.save()
        return user

    def get_question_by_quiz(self, question, quiz):
        try:
            quiz.question.get(id=question.id)
        except ObjectDoesNotExist:
            raise ValidationError(f'There is no question {question.id} in quiz {quiz.id}', code=400)
        return question

    # Method for checking suit answers if it needs
    def check_answer_by_question(self, question, answer):
        return True

    def beauty_answer(self, answers):
        result = {}

        def fill_result(answer):
            if answer.quiz.name not in result:
                result[answer.quiz.name] = list()
            result[answer.quiz.name].append(
                {
                    'question': answer.question.text,
                    'answer': answer.answer
                }
            )

        list(map(
            fill_result,
            answers
        ))
        return result

    def answer_creater(self, dictQA):
        question, answer = dictQA['question'], dictQA['answer']
        question = self.get_question_by_quiz(question, self.context['quiz'])
        # Can perform if it needed
        self.check_answer_by_question(question, answer)

        inst = Answer(
            user_id=self.context['user_id'],
            quiz=self.context['quiz'],
            question=question,
            answer=answer
        )
        return inst


