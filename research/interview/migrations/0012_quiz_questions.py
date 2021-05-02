# Generated by Django 2.2.10 on 2021-04-30 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0011_remove_quiz_questions'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='questions',
            field=models.ManyToManyField(related_name='quiz', to='interview.Question'),
        ),
    ]