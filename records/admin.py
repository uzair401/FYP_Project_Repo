from django.contrib import admin
from .models import ExamRecord, StudentExamRecord, StudentSemesterRecord

@admin.register(ExamRecord)
class ExamRecordAdmin(admin.ModelAdmin):
    list_display = ('record_id', 'record_name', 'record_year', 'examiner', 'program', 'batch')
    search_fields = ('record_name',)
    list_filter = ('program', 'batch')

@admin.register(StudentExamRecord)
class StudentExamRecordAdmin(admin.ModelAdmin):
    list_display = ( 'internal_marks_obtained', 'mid_marks_obtained', 'final_marks_obtained', 'percentage_per_course', 'gpa_per_course', 'exam_record', 'program', 'semester', 'course', 'student')
    search_fields = ('student__first_name', 'student__last_name', 'course__course_name')
    list_filter = ('program', 'semester', 'course')

@admin.register(StudentSemesterRecord)
class StudentSemesterRecordAdmin(admin.ModelAdmin):
    list_display = ( 'total_semester_marks', 'semester_obtained_marks', 'percentage', 'gpa_per_semester', 'cgpa', 'status', 'student_exam_rec', 'student')
    search_fields = ('student__first_name', 'student__last_name')
    list_filter = ('status',)
