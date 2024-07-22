# students/urls.py
from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.student, name='Student_dashboard'),
    path('add_student/', views.add_student, name='add_student'),
    path('update/<int:student_id>/', views.student_update, name='student_update'),
    path('delete/<int:student_id>/', views.student_delete, name='student_delete')
]
