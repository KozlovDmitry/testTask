from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^question/$', QuestionList.as_view()),
    url(r'^question/(?P<pk>[0-9]+)/$', QuestionDetail.as_view()),
    url(r'^quiz/$', QuizList.as_view()),
    url(r'^quiz/(?P<pk>[0-9]+)/$', QuizDetail.as_view()),
    url(r'^availablequiz/$', AvailableQuizList.as_view()),
    url(r'^availablequiz/(?P<pk>[0-9]+)/$', AvailableQuizDetail.as_view()),
    url(r'^passquiz/$', PassQuiz.as_view()),
    url(r'^passedquiz/(?P<pk>[0-9]+)/$', PassedQuiz.as_view()),
]

