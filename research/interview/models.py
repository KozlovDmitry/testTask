from django.db import models


class Question(models.Model):
    q_type = [
        ('ответ текстом', 'ответ текстом'),
        ('ответ с выбором одного варианта', 'ответ с выбором одного варианта'),
        ('ответ с выбором нескольких вариантов', 'ответ с выбором нескольких вариантов'),
    ]

    text = models.TextField()
    type = models.CharField(choices=q_type, max_length=100)
    quiz = models.ManyToManyField('Quiz', related_name='question')


class Quiz(models.Model):
    name = models.TextField()
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name


class Answer(models.Model):
    answer = models.TextField()
    question = models.ForeignKey('Question', related_name='answer', on_delete=models.CASCADE)
    quiz = models.ForeignKey('Quiz', related_name='answer', on_delete=models.CASCADE)
    user_id = models.ForeignKey('UserOfResearch', related_name='answer', on_delete=models.CASCADE)


class UserOfResearch(models.Model):
    user_id = models.IntegerField(primary_key=True)


