from django.db import models


class Question(models.Model):
    name = models.TextField()
    type = models.ForeignKey('QuestionType', related_name='question', on_delete=models.CASCADE)
    question_option = models.ManyToManyField('QuestionOption', related_name='question')

    def __str__(self):
        return self.name


class QuestionType(models.Model):
    q_type = [
        ('ответ текстом', 'text'),
        ('ответ с выбором одного варианта', 'one_choose'),
        ('ответ с выбором нескольких вариантов', 'many_choose'),
    ]

    type = models.CharField(max_length=100, choices=q_type)

    def __str__(self):
        return self.type


class QuestionOption(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    name = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True, default=None)
    active = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True, default=None)
    questions = models.ManyToManyField('Question', related_name='quiz')

    def __str__(self):
        return self.name


class Answer(models.Model):
    answer = models.TextField()
    question = models.ForeignKey('Question', related_name='answer', on_delete=models.CASCADE)
    quiz = models.ForeignKey('Quiz', related_name='answer', on_delete=models.CASCADE)
    user_id = models.ForeignKey('UserOfResearch', related_name='answer', on_delete=models.CASCADE)

    def __str__(self):
        if len(self.answer) > 30:
            return self.answer[30:] + '...'
        return self.answer


class UserOfResearch(models.Model):
    user_id = models.IntegerField(primary_key=True)
    passed_quiz = models.ManyToManyField('Quiz', related_name='user_id', blank=True, null=True)

    def __str__(self):
        return str(self.user_id)

