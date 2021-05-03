from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^questiontype/$', QuestionTypeList.as_view()),
    url(r'^questiontype/(?P<pk>[0-9]+)/$', QuestionTypeDetail.as_view()),
    url(r'^questionoption/$', QuestionOptionList.as_view()),
    url(r'^questionoption/(?P<pk>[0-9]+)/$', QuestionOptionDetail.as_view()),
    url(r'^question/$', QuestionList.as_view()),
    url(r'^question/(?P<pk>[0-9]+)/$', QuestionDetail.as_view()),
    url(r'^quiz/$', QuizList.as_view()),
    url(r'^quiz/(?P<pk>[0-9]+)/$', QuizDetail.as_view()),
    url(r'^availablequiz/$', AvailableQuizList.as_view()),
    url(r'^passedquiz/(?P<pk>[0-9]+)/$', PassedQuiz.as_view()),
    url(r'^answertoquiz/(?P<pk>[0-9]+)/$', AnswerToQuiz.as_view()),
]
