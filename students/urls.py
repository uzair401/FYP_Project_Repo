# students/urls.py
from django.urls import path
from . import views



app_name = 'students'

urlpatterns = [
    # path('<int:course_id>/', views.student, name='student'),
    path('', views.student, name= "Student_dashboard"),
    # path('get_programs_and_batches/', get_programs_and_batches, name='get_programs_and_batches'),
    path('add_student/', views.add_student, name='add_student'),
    path('<int:student_id>/update/', views.student_update, name='student_update'),
    path('<int:student_id>/delete/', views.student_delete, name='student_delete')
]

    # path('add_student/', views.add_student, name='add_student'),

    # path('<int:id>/', views.student_detail, name='student_detail'),

