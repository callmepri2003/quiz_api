from django.contrib import admin

# Register your models here.
from .models import Student, QuizAttempt, QuestionAttempt, QuizContent

admin.site.register(Student)
admin.site.register(QuizAttempt)
admin.site.register(QuestionAttempt)
admin.site.register(QuizContent)