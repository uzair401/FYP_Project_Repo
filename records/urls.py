from django.urls import path
from . import views

app_name = 'records'

urlpatterns = [
    path('', views.exam_dashboard, name='Exam_dashboard'),
    path('add_record/', views.add_record, name='add_record'),
    path('batches/<int:exam_record_id>/', views.batches, name='batches'),
    path('update_batch/<int:id>/', views.update_batch, name="update_batch"),
    path('semesters/<int:batch_id>/<int:exam_record_id>/', views.semesters, name='semesters'),  
    path('courses/<int:semester_id>/', views.courses, name='courses'),
    path('course/<int:course_id>/semester/<int:semester_id>/records/', views.course_student_records, name='course_student_records'),
    # path('<int:id>/', views.record_detail, name='record_detail'),

]
