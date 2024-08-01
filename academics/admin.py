from django.contrib import admin
from .models import Department, Program, Semester, Course, Batch
from .forms import ProgramForm, SemesterForm, CourseForm, BatchForm


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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'Faculty':
            return qs.filter(department_id=request.user.department.department_id)
        return qs
    
@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ( 'program_name', 'program_code', 'number_of_semesters', 'program_description', 'department')
    search_fields = ('program_name', 'program_code')
    list_filter = ('department',)
    inlines = [SemesterInline, BatchInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'Faculty':
            return qs.filter(department_id=request.user.department.department_id)
        return qs
@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ( 'semester_number', 'semester_category', 'program')
    search_fields = ('semester_number', 'semester_category', 'program__program_name')
    list_filter = ('program', 'semester_category')
    inlines = [CourseInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'Faculty':
            return qs.filter(program__department=request.user.department)
        return qs

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ( 'course_name', 'course_code', 'credit_hours', 'internal_marks', 'mid_marks', 'final_marks', 'course_description', 'semester')
    search_fields = ('course_name', 'course_code')
    list_filter = ('semester__program',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'Faculty':
            return qs.filter(semester__program__department=request.user.department)
        return qs

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('batch_name', 'batch_number', 'batch_year', 'batch_session_start','batch_session_end','batch_status', 'program')
    search_fields = ('batch_name', 'program__program_name', 'batch_number')
    list_filter = ('program',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'Faculty':
            return qs.filter(program__department=request.user.department)
        return qs