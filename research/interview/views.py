from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .my_helper import MyHelper
from .serializers import *
from .models import *


class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAdminUser]


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionAdditionalSerializer
    permission_classes = [permissions.IsAdminUser]


class QuizList(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAdminUser]


class QuizDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizAdditionalSerializer
    permission_classes = [permissions.IsAdminUser]


class AvailableQuizList(generics.ListAPIView, MyHelper):
    serializer_class = QuizSerializer

    def get_queryset(self):
        return self.get_active_quizs()


class AvailableQuizDetail(APIView, MyHelper):
    def get(self, request, *args, **kwargs):
        my_helper = MyHelper()
        try:
            quiz = my_helper.get_active_quiz_by_pk(self.kwargs['pk'])
        except ValidationError as e:
            return Response(e.detail[0], status=status.HTTP_400_BAD_REQUEST)
        questions = [{
            'id': item.id,
            'type': item.type,
            'text': item.text
        } for item in Question.objects.filter(quiz=quiz)]

        return Response(questions)


class PassQuiz(APIView, MyHelper):
    def post(self, request):
        if 'answers' not in request.data:
            return Response('answers should be exist', status=status.HTTP_400_BAD_REQUEST)
        else:
            answers_ser = MyCustomeSerializer(data=request.data.get('answers', []), many=True)

        if answers_ser.is_valid():
            general_ser = AnswerSerializer(
                data={
                    'user_id': request.data.get('user_id', None),
                    'quiz': request.data.get('quiz', None),
                },
                context={'answers': answers_ser.validated_data}
            )
        else:
            return Response(answers_ser.errors, status=status.HTTP_400_BAD_REQUEST)

        if general_ser.is_valid():
            general_ser.create(validated_data=general_ser.validated_data)
            return Response(general_ser.data)
        return Response(general_ser.errors, status=status.HTTP_400_BAD_REQUEST)


class PassedQuiz(APIView, MyHelper):
    def get(self, request, *args, **kwargs):
        my_helper = MyHelper()
        queryset = Answer.objects.filter(user_id=kwargs['pk'])
        if queryset.count() == 0:
            return Response('No passed quiz', status=status.HTTP_404_NOT_FOUND)
        return Response(my_helper.beauty_answer(queryset))


