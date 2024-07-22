# academics/urls.py
from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [

    # path('<int:course_id>/', views.student, name='student'),
    path('', views.department, name= "Department_dashboard"),
    # path('get_programs_and_batches/', get_programs_and_batches, name='get_programs_and_batches'),
    path('add_department/', views.add_department, name='add_department'),
    path('<int:department_id>/update/', views.department_update, name='department_update'),
    path('<int:department_id>/delete/', views.department_delete, name='department_delete')
    # path('add_program/', views.add_program, name="add_program"),
    # path('program/update/<int:pk>/', views.update_program, name='update_program'),
    # path('program/delete/<int:pk>/', views.delete_program, name='delete_program'),
    # path('batch/<int:program_id>/', views.batch, name="batch"),
    # path('batch/update/<int:pk>/', views.update_batch, name='update_batch'),
    # path('batch/delete/<int:pk>/', views.delete_batch, name='delete_batch'),
    # path('semester/<int:program_id>/', views.semester, name="semester"),
    # path('semester/update/<int:pk>/', views.update_semester, name='update_semester'),
    # path('semester/delete/<int:pk>/', views.delete_semester, name='delete_semester'),
    # path('course/<int:semester_id>/', views.course, name="course"),
    # path('course/update/<int:pk>/', views.update_course, name='update_course'),
    # path('course/delete/<int:pk>/', views.delete_course, name='delete_course'),
]
