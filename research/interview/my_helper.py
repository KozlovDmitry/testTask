from rest_framework.exceptions import ValidationError
from rest_framework import status
from .models import QuestionOption, QuestionType, Question, Quiz, UserOfResearch


class MyHelper:
    def get_create_question_option(self, question_option):
        name = question_option.name if isinstance(question_option, QuestionOption) else question_option['name']
        try:
            q_option = QuestionOption.objects.get(name__iexact=name)
            return q_option
        except:
            new_question = QuestionOption(name=name)
            new_question.save()
            return new_question

    def check_relation_q_type_q_option(self, q_type, q_option):
        if type(q_option).__name__ == 'ManyRelatedManager':
            count_q_option = q_option.count()
            q_option = q_option.all()
        else:
            count_q_option = len(q_option)
        if q_type.type == "ответ текстом" and count_q_option > 0:
            raise ValidationError('You tried set question_option in field "ответ текстом"',
                                  code=status.HTTP_400_BAD_REQUEST)
        if q_type.type != "ответ текстом" and count_q_option == 0:
            raise ValidationError('You have to set at least one question_option', code=status.HTTP_400_BAD_REQUEST)
        return (q_type, q_option)

    def get_create_q_type(self, type):
        type = type.type if isinstance(type, QuestionType) else type['type']
        try:
            q_type = QuestionType.objects.get(type=type)
        except:
            q_type = QuestionType(type=type)
            q_type.save()
        return q_type

    def is_parameter_transfer(self, name):
        if name is None:
            raise ValidationError('For CREATE method field name is mandatory', code=status.HTTP_400_BAD_REQUEST)
        return name

    def get_active_quiz(self, pk):
        try:
            quiz = Quiz.objects.get(pk=pk)
        except:
            raise ValidationError(f"Quiz {pk} hasn't found", code=status.HTTP_404_NOT_FOUND)
        if quiz.active is False:
            raise ValidationError(f"Quiz {pk} isn't active", code=status.HTTP_400_BAD_REQUEST)
        return quiz

    def get_user(self, request):
        if 'user_id' not in request.data:
            raise ValidationError('You have to transfer user_id', code=status.HTTP_400_BAD_REQUEST)
        if not isinstance(request.data['user_id'], int):
            raise ValidationError('user_id should be integer', code=status.HTTP_400_BAD_REQUEST)
        try:
            user_id = UserOfResearch.objects.get(user_id=request.data['user_id'])
        except:
            user_id = UserOfResearch(user_id=request.data['user_id'])
            user_id.save()
        return user_id

    def get_answers(self, request):
        if 'answers' not in request.data:
            raise ValidationError('You have to transfer answers', code=status.HTTP_400_BAD_REQUEST)
        return request.data['answers']

    def get_validate_answer(self, qna_tuple):
        answer, question_options = qna_tuple
        if answer not in question_options:
            raise ValidationError(f"You have chosen unavailable option - {answer}, please choose from {question_options}",
                                  code=status.HTTP_400_BAD_REQUEST)
        return answer

    def is_answer_correct(self, qna_dict):
        question = Question.objects.get(pk=qna_dict['question'])
        answer = qna_dict['answer']
        if question.type.type in ['ответ с выбором одного варианта', 'ответ с выбором нескольких вариантов']:
            question_options = [item.name.lower() for item in question.question_option.all()]
            answer = answer.lower()

            if question.type.type == 'ответ с выбором одного варианта':
                validate_answer = self.get_validate_answer((answer, question_options))
            else:
                answers = [item.strip() for item in answer.split(',')]
                validate_answer = list(map(
                    self.get_validate_answer,
                    list(zip(answers, [question_options for i in answers]))
                ))
                validate_answer = ','.join(validate_answer)
        else:
            validate_answer = answer
        return validate_answer

    def check_get_question(self, question, quiz):
        if question in [item.id for item in quiz.questions.all()]:
            return question
        raise ValidationError(f"There is no question {question} in quiz {quiz.id}", code=status.HTTP_400_BAD_REQUEST)
