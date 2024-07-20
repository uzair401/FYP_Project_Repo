from django.contrib import admin
from .models import Student, Enrollment
from academics.models import Program, Semester, Course, Batch
from records.models import StudentExamRecord, StudentSemesterRecord

class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0

class StudentExamRecordInline(admin.TabularInline):
    model = StudentExamRecord
    extra = 0

class StudentSemesterRecordInline(admin.TabularInline):
    model = StudentSemesterRecord
    extra = 0

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ( 'first_name', 'last_name', 'father_name', 'date_of_birth', 'registration_number', 'enrollment_year', 'status', 'department', 'program', 'batch')
    search_fields = ('first_name', 'last_name', 'registration_number')
    list_filter = ('department', 'program', 'status')
    inlines = [EnrollmentInline, StudentExamRecordInline, StudentSemesterRecordInline]

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('enrollment_id', 'student', 'course', 'semester')
    search_fields = ('student__first_name', 'student__last_name', 'course__course_name')
    list_filter = ('student__program', 'course__semester')

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('batch_id', 'batch_name', 'batch_year', 'batch_number', 'batch_session', 'program')
    search_fields = ('batch_name', 'batch_session')
    list_filter = ('program',)
