from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

from .models import QuizAttempt, QuizContent, Student

import base64
import json

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import QuestionDeserializer, QuizContentSerializer, StudentSerializer

# Create your views here.

@api_view()
@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def authenticate_api_view(request):
    data = {
        'user': str(request.user),
        'auth': str(request.auth)
    }
    quiz_start = QuizAttempt(request)
    return Response(data)

@api_view()
@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def new_quiz_view(request):
    data = {}
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        username = base64.urlsafe_b64decode(auth_header.split()[1]).decode('UTF-8').split(':')[0]
    
        try:
            new_quiz_attempt = QuizAttempt(student = Student.objects.get(user = User.objects.get(username = username)))
            
        except:
            return Response({'Error': "Student doesn't exist."}, status = status.HTTP_400_BAD_REQUEST)
        
        new_quiz_attempt.save()

        data = {
            'quiz_attempt_id': new_quiz_attempt.id,
            'quiz': {}
        }
        
        counter = 1
        for content in QuizContent.objects.all():
            data['quiz']['q'+str(counter)] = QuizContentSerializer(content).data
            counter += 1
    return Response(data)

@api_view()
@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def submit_quiz_view(request):
    #Create new question attempt and add it to the quiz attempt
    # The dict should look something like this after 
    # being converted from JSON
    data = {}
    
    submittedData = json.loads(request.body)
    # Deserialize the results into question attempts
    questions = submittedData['submitted_answers'].keys()
    for question in questions:
        questionAttemptObj = QuestionDeserializer(question, submittedData['submitted_answers'][question], submittedData['quiz_attempt_id'])
        questionAttemptObj.save()
    
    data = {'score': QuizAttempt.objects.get(id = submittedData['quiz_attempt_id']).score}
    return Response(data)


@api_view()
@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def students_info_view(request):
    data = {}
    for student in Student.objects.all():
        data[student.id] = {'name': str(student.user.first_name) + ' ' + str(student.user.last_name), 'average_score': student.average_score, 'attempted_quizzes': []}
    
    for key in data.keys():
        quiz_attempts = QuizAttempt.objects.filter(student = Student.objects.get(id = key))
        for quiz in quiz_attempts:
            data[key]['attempted_quizzes'].append({'quiz_attempt_id': quiz.id, 'quiz_score': quiz.score, 'taken_at': quiz.date_time})
        
    return Response(data)