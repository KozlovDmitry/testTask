# Generated by Django 2.2.10 on 2021-04-30 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0010_auto_20210430_1722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='questions',
        ),
    ]
