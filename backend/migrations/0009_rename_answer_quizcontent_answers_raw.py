# Generated by Django 4.1.4 on 2022-12-19 04:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_alter_student_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quizcontent',
            old_name='answer',
            new_name='answers_raw',
        ),
    ]