from django.shortcuts import render
import requests
from quiz_api.settings import quiz_api_username as username, quiz_api_password as password
# Create your views here.

import json
from backend.serializers import QuestionDeserializer

new_quiz_endpoint = '/api/new_quiz/'
submit_quiz_endpoint ='/api/submit_quiz/'
students_info_endpoint = '/api/students_info/'

def home_view(request):
    context = {
        'phase': 'initial'
    }
    current_host = request.build_absolute_uri('/')[:-1]
    if 'new_quiz' in request.GET.keys() and request.GET['new_quiz']:
        
        quiz = requests.get(current_host + new_quiz_endpoint, auth=(username, password))
        
        context['phase'] = 'new_quiz'
        context['quiz'] = quiz.json()['quiz']
        context['questions'] = context['quiz'].keys()
        context['quiz_attempt_id'] = quiz.json()['quiz_attempt_id'] 
    elif 'quiz_attempt_id' in request.POST:
    
        data = {
            'quiz_attempt_id': request.POST['quiz_attempt_id'],
            'submitted_answers' : {}
        }

        # I need to do some custom string manipulation here
        # JSON isn't converting the array of submitted answers
        # to python lists correctly
        postData = json.loads(str(request.POST)[12:-1].replace('\'', '"'))
        print(postData)


        for key in postData.keys():
            if not key == 'csrfmiddlewaretoken' and not key == 'quiz_attempt_id':
                data['submitted_answers'][key] = postData[key]
                
        
        data['submitted_answers']
        results = requests.get(current_host + submit_quiz_endpoint, auth=(username, password), json=data)
        context['phase'] = 'results'
        context['score'] = results.json()['score']
        # for key in request.POST.keys():
        #     if not key == 'csrfmiddlewaretoken' and not key == 'quiz_attempt_id':
        #         QuestionDeserializer(int(key), request.POST[key], request.POST['quiz_attempt_id'])
    return render(request, 'index.html', context)

def student_information_view(request):
    current_host = request.build_absolute_uri('/')[:-1]
    print(requests.get(current_host + students_info_endpoint, auth = (username, password)).text)
    context = {
        'students': requests.get(current_host + students_info_endpoint, auth = (username, password)).json()
    }
    return render(request, 'students.html', context)


def api_reference_view(request):
    context = {}
    return render(request, 'api_reference.html', context)