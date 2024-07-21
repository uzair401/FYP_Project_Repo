# students/urls.py
from django.urls import path
from . import views
from .views import student, add_student


app_name = 'students'

urlpatterns = [
    # path('<int:course_id>/', views.student, name='student'),
    path('', views.student, name= "Student_dashboard"),
    # path('get_programs_and_batches/', get_programs_and_batches, name='get_programs_and_batches'),
    path('add_student/', add_student, name='add_student'),
    # path('add_student/', views.add_student, name='add_student'),

    # path('<int:id>/', views.student_detail, name='student_detail'),
]
