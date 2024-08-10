from django.urls import path
from . import views

app_name = 'records'

urlpatterns = [
    path('', views.exam_dashboard, name='Exam_dashboard'),
    path('dash', views.dash, name="dash"),
    path('add_record/', views.add_record, name='add_record'),
    path('batches/<int:exam_record_id>/', views.batches, name='batches'),
    path('update_batch/<int:id>/', views.update_batch, name="update_batch"),
    path('semesters/<int:batch_id>/<int:exam_record_id>/', views.semesters, name='semesters'),  
    path('courses/<int:semester_id>/<int:batch_id>/', views.courses, name='courses'),
    path('course/<int:course_id>/semester/<int:semester_id>/batch/<int:batch_id>/records/', views.course_student_records, name='course_student_records'),
    path('update_student_record/', views.update_student_record, name='update_student_record'),
    path('reset_student_record/', views.reset_student_record, name='reset_student_record'),
    path('records-dashboard', views.semesters_rec_dash, name='semester_record_dashboard'),
    path('batch/<int:exam_record_id>/', views.records_batches, name='records_batches'),
    path('semester/<int:batch_id>/<int:exam_record_id>/', views.records_semester, name='record_semester'),
    path('records/semester-results/<int:exam_record_id>/<int:semester_id>/<int:batch_id>/', views.semester_results, name='semester_results'),
    path('courses-records/', views.courses_rec_dash, name='courses_record_dashboard'),
    path('course-batch/<int:exam_record_id>/', views.course_records_batches, name='course_records_batches'),
    path('course-semester/<int:batch_id>/<int:exam_record_id>/', views.courses_semesters, name='courses_semesters'),
    path('courses-courses/<int:semester_id>/<int:batch_id>/', views.courses_record, name='courses_record'),
    path('course-results/<int:semester_id>/<int:batch_id>/<int:course_id>/', views.course_results, name='course_results'),
    path('transcript/program/', views.transcript_program_selection, name='Transcript_Program'),
    path('transcript/batch/<int:program_id>/', views.transcript_batch, name='Transcript_Batch'),
    path('transcript/students/<int:batch_id>/', views.transcript_student, name='Transcript_students'),
    path('transcript/<int:student_id>/', views.student_transcript, name='student_transcript'),

]
