from django.contrib import admin
from .models import *


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type']

@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type']

@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active', 'start_date', 'end_date', 'description']

@admin.register(UserOfResearch)
class UserOfResearchAdmin(admin.ModelAdmin):
    list_display = ['user_id']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'quiz', 'question', 'user_id']
    list_filter = ['user_id', 'quiz']

#
#
# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ['short_name']
#     # list_filter = ['question_type']
# #
# #
# @admin.register(QuestionType)
# class QuestionTypeAdmin(admin.ModelAdmin):
#     list_display = ['id', 'type']
# #
# #

#
#

#
#
# @admin.register(AnswerOptionSet)
# class AnswerOptionSetAdmin(admin.ModelAdmin):
#     list_display = ['name']
#
#
# @admin.register(AnswerOption)
# class AnswerOptionAdmin(admin.ModelAdmin):
#     list_display = ['name']