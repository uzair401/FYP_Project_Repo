from django.contrib import admin
from .models import ExamRecord, StudentExamRecord, StudentSemesterRecord, ExamEnrollment

@admin.register(ExamRecord)
class ExamRecordAdmin(admin.ModelAdmin):
    list_display = ('record_name', 'record_year', 'examiner', 'program', 'exam_date', 'session')
    search_fields = ('record_name',)
    list_filter = ('program', )
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'Faculty':
            return qs.filter(program__department=request.user.department)
        return qs
@admin.register(StudentExamRecord)
class StudentExamRecordAdmin(admin.ModelAdmin):
    list_display = (                      
        'student',  
        'course',                        
        'program',                       
        'semester',        
        'internal_marks',
        'mid_marks',
        'final_marks',
        'total_marks',
        'gpa_per_course',
        'remarks',
        'is_repeated',  # Added is_repeated here
        'exam_record',                                              
    )
    search_fields = ('student__first_name', 'student__last_name', 'course__course_name')
    list_filter = ('program', 'semester', 'course')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'Faculty':
            return qs.filter(program__department=request.user.department)
        return qs
@admin.register(StudentSemesterRecord)
class StudentSemesterRecordAdmin(admin.ModelAdmin):
    list_display = (
        'student_exam_rec',                
        'total_semester_marks',
        'semester_obtained_marks',
        'percentage',
        'gpa_per_semester',
        'cgpa',
        'remarks',
        'student',                       
        'semester',                     
        'exam_record'                    
    )
    search_fields = ('student__first_name', 'student__last_name')
    list_filter = ('remarks', 'semester', 'exam_record')
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'Faculty':
            return qs.filter(semester__program__department=request.user.department)
        return qs
    
@admin.register(ExamEnrollment)
class ExamEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('exam_record', 'batch', 'semester')
    search_fields = ('exam_record__record_name', 'batch__batch_id', 'semester__semester_number')
    list_filter = ('exam_record', 'batch', 'semester')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'Faculty':
            return qs.filter(exam_record__program__department=request.user.department)
        return qs