from django.urls import path

from .views import home_view, student_information_view, api_reference_view

urlpatterns = [
    path('', home_view),
    path('students', student_information_view),
    path('reference', api_reference_view)
]