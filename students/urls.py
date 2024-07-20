# students/urls.py
from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('<int:course_id>/', views.student, name='student'),
    # path('<int:id>/', views.student_detail, name='student_detail'),
]
