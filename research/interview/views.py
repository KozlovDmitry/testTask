from rest_framework import generics, authentication, permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from .models import *



class QuestionTypeList(generics.ListCreateAPIView):
    queryset = QuestionType.objects.all()
    serializer_class = QuestionTypeSerializer
    permission_classes = [permissions.IsAdminUser]



class QuestionTypeDetail(generics.RetrieveDestroyAPIView):
    queryset = QuestionType.objects.all()
    serializer_class = QuestionTypeSerializer
    permission_classes = [permissions.IsAdminUser]


class QuestionOptionList(generics.ListCreateAPIView):
    queryset = QuestionOption.objects.all()
    serializer_class = QuestionOptionSerializer
    permission_classes = [permissions.IsAdminUser]


class QuestionOptionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuestionOption.objects.all()
    serializer_class = QuestionOptionSerializer
    permission_classes = [permissions.IsAdminUser]


class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAdminUser]


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAdminUser]


class QuizList(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAdminUser]


class QuizDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAdminUser]


class AvailableQuizList(generics.ListAPIView):
    queryset = Quiz.objects.filter(active=True)
    serializer_class = AvailableQuizSerializer


class PassedQuiz(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = PassedQuizSerializer

    def list(self, request, *args, **kwargs):
        pk = kwargs['pk']
        try:
            user = UserOfResearch.objects.get(pk=pk)
        except:
            return Response(f"User {pk} hasn't been found", status=status.HTTP_404_NOT_FOUND)

        quizzes = [{
            'id': quiz.id,
            'name': quiz.name,
            'answers': Answer.objects.filter(user_id=user, quiz=quiz)
        }
            for quiz in Quiz.objects.filter(user_id=user)]
        if len(quizzes) == 0:
            return Response('There are no any passed quiz', status=status.HTTP_200_OK)
        serializer = PassedQuizSerializer(quizzes, many=True, context={"user": user})
        return Response(serializer.data)


class AnswerToQuiz(generics.ListCreateAPIView, MyHelper):
    queryset = Question.objects.all()
    serializer_class = AnswerToQuizSerializer

    def list(self, request, *args, **kwargs):
        quiz = self.get_active_quiz(kwargs['pk'])
        serializer = AnswerToQuizSerializer(quiz)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        answers = self.get_answers(request)
        serializer = AnswerSerializer(data=answers, many=True)

        if serializer.is_valid():
            user_id = self.get_user(request)
            quiz = self.get_active_quiz(kwargs['pk'])

            if quiz in user_id.passed_quiz.all():
                return Response('You have already passed this quiz', status=status.HTTP_208_ALREADY_REPORTED)

            list(map(
                self.is_answer_correct,
                answers
            ))

            answer_instances = list(map(
                lambda item: Answer(
                    answer=item['answer'],
                    question_id=self.check_get_question(item['question'], quiz),
                    user_id=user_id,
                    quiz=quiz,
                ),
                answers
            ))
            Answer.objects.bulk_create(answer_instances)
            user_id.passed_quiz.add(quiz)

            return Response(serializer.data)
        return Response('Bad request', status=status.HTTP_400_BAD_REQUEST)



