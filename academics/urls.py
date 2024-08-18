# academics/urls.py
from django.urls import path
from .import views

app_name = 'academics'

urlpatterns = [

    # path('<int:course_id>/', views.student, name='student'),
    path('department', views.department, name= "Department_dashboard"),
    path('add_department/', views.add_department, name='add_department'),
    path('<int:department_id>/update/', views.department_update, name='department_update'),
    path('<int:department_id>/delete/', views.department_delete, name='department_delete'),
    path('program/', views.program, name= "Program_dashboard"),
    path('add_program/', views.add_program, name='add_program'),
    path('program/<int:program_id>/update/', views.program_update, name='program_update'),
    path('program/<int:program_id>/delete/', views.program_delete, name='program_delete'),
    path('semesters/<int:program_id>/', views.semester_filtered, name='semester_filtered'),
    path('add_semester/', views.add_semester, name='add_semester'),
    path('semester/<int:semester_id>/update/', views.semester_update, name='semester_update'),
    path('semester/<int:semester_id>/delete/', views.semester_delete, name='semester_delete'),
    path('course/', views.course, name= "Course_dashboard"),
    path('add_course/', views.add_course, name='add_course'),
    path('course/<int:course_id>/update/', views.course_update, name='course_update'),
    path('course/<int:course_id>/delete/', views.course_delete, name='course_delete'),
    path('batch/', views.batch, name= "Batch_dashboard"),
    path('add_batch/', views.add_batch, name='add_batch'),
    path('batch/<int:batch_id>/update/', views.batch_update, name='batch_update'),
    path('batch/<int:batch_id>/delete/', views.batch_delete, name='batch_delete'),
 ]
