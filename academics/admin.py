from django.contrib import admin
from .models import Department, Program, Semester, Course, Batch

class ProgramInline(admin.TabularInline):
    model = Program
    extra = 0

class SemesterInline(admin.TabularInline):
    model = Semester
    extra = 0

class CourseInline(admin.TabularInline):
    model = Course
    extra = 0

class BatchInline(admin.TabularInline):
    model = Batch
    extra = 0

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ( 'department_name','department_discipline', 'department_description')
    search_fields = ('department_name', 'department_discipline')
    inlines = [ProgramInline]

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ( 'program_name', 'program_code', 'number_of_semesters', 'program_description', 'department')
    search_fields = ('program_name', 'program_code')
    list_filter = ('department',)
    inlines = [SemesterInline, BatchInline]

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ( 'semester_number', 'semester_category', 'program')
    search_fields = ('semester_number', 'semester_category', 'program__program_name')
    list_filter = ('program', 'semester_category')
    inlines = [CourseInline]

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ( 'course_name', 'course_code', 'credit_hours', 'internal_marks', 'mid_marks', 'final_marks', 'course_description', 'semester')
    search_fields = ('course_name', 'course_code')
    list_filter = ('semester__program',)
