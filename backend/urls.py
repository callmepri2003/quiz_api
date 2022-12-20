# Arguably unnecessary to create a separate urls file for an app of this scale
# However, it's easier to commit to best practises regardless than to completely 
# refactor the app to add functionality down the road.

from django.contrib import admin
from django.urls import path, include

from .views import authenticate_api_view, new_quiz_view, submit_quiz_view, students_info_view

urlpatterns = [
    path('authenticate/', authenticate_api_view),
    path('new_quiz/', new_quiz_view),
    path('submit_quiz/', submit_quiz_view),
    path('students_info/', students_info_view),
    
]