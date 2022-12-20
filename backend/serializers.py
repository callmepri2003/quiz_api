from rest_framework import serializers
from .models import QuizContent, QuestionAttempt, QuizAttempt, Student
import json
# class QuizContentSerializer(serializers.Serializer):
#     question = serializers.CharField(max_length = 1000)
#     answer = serializers.CharField(max_length = 1000)
#     percentage_correct


class PercentageCorrectField(serializers.RelatedField):
    def to_representation(self, value):
        return '%d' % (value)

class QuizContentSerializer(serializers.ModelSerializer):
    percentage_correct = PercentageCorrectField(read_only = True)
    
    class Meta:
        model = QuizContent
        fields = ['id', 'question', 'answers', 'percentage_correct']

def QuestionDeserializer(question_id, submitted_answers, quiz_id):
    quiz_attempt = QuizAttempt.objects.get(id=quiz_id)
    quiz_content = QuizContent.objects.get(id=question_id)
    print(submitted_answers)
    new_question_attempt = QuestionAttempt(quiz_attempt = quiz_attempt, quiz_content = quiz_content, submitted_answer = json.dumps(submitted_answers))
    
    return new_question_attempt

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['average_score']