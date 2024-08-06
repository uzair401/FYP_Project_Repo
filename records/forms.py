
from django import forms
from .models import ExamRecord, StudentExamRecord, StudentSemesterRecord, ExamEnrollment
from academics.models import Program, Course, Semester ,Batch
from students.models import Student
from core.models import User

class ExamRecordForm(forms.ModelForm):
    class Meta:
        model = ExamRecord
        fields = ['record_name', 'record_year', 'exam_date', 'session', 'examiner', 'program']
        widgets = {
            'record_name': forms.TextInput(attrs={'class': 'form-control'}),
            'record_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'exam_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'session': forms.Select(choices=ExamRecord.SESSION_CHOICES, attrs={'class': 'form-control'}),
            'examiner': forms.Select(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        department_id = kwargs.pop('department_id', None)  # Remove department_id from kwargs
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            if user.role == 'Admin':
                self.fields['examiner'].queryset = User.objects.all()
                self.fields['program'].queryset = Program.objects.all()
            elif user.role == 'Faculty':
                self.fields['examiner'].queryset = User.objects.filter(department=user.department)
                self.fields['program'].queryset = Program.objects.filter(department=user.department)
class StudentExamRecordForm(forms.ModelForm):
    class Meta:
        model = StudentExamRecord
        fields = ['internal_marks', 'mid_marks', 'final_marks',  'gpa_per_course', 'remarks', 'exam_record', 'program', 'semester', 'course', 'student']
        widgets = {
            'internal_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'mid_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'final_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'gpa_per_course': forms.NumberInput(attrs={'class': 'form-control'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control'}),
            'exam_record': forms.Select(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            if user.role == 'Admin':
                self.fields['program'].queryset = Program.objects.all()
                self.fields['semester'].queryset = Semester.objects.all()
                self.fields['course'].queryset = Course.objects.all()
                self.fields['student'].queryset = Student.objects.all()
            elif user.role == 'Faculty':
                self.fields['program'].queryset = Program.objects.filter(department=user.department)
                program_id = self.initial.get('program') or self.data.get('program')
                if program_id:
                    self.fields['semester'].queryset = Semester.objects.filter(program_id=program_id)
                    self.fields['course'].queryset = Course.objects.filter(program_id=program_id)
                    self.fields['student'].queryset = Student.objects.filter(department=user.department)

class StudentSemesterRecordForm(forms.ModelForm):
    class Meta:
        model = StudentSemesterRecord
        fields = ['total_semester_marks', 'semester_obtained_marks', 'percentage', 'gpa_per_semester', 'cgpa', 'remarks', 'exam_record', 'student', 'semester']
        widgets = {
            'total_semester_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'semester_obtained_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'percentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'gpa_per_semester': forms.NumberInput(attrs={'class': 'form-control'}),
            'cgpa': forms.NumberInput(attrs={'class': 'form-control'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control'}),
            'exam_record': forms.Select(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            if user.role == 'Admin':
                self.fields['student'].queryset = Student.objects.all()
                self.fields['semester'].queryset = Semester.objects.all()
                self.fields['exam_record'].queryset = ExamRecord.objects.all()
            elif user.role == 'Faculty':
                self.fields['student'].queryset = Student.objects.filter(department=user.department)
                program_id = self.initial.get('program') or self.data.get('program')
                if program_id:
                    self.fields['semester'].queryset = Semester.objects.filter(program_id=program_id)
                    self.fields['exam_record'].queryset = ExamRecord.objects.filter(program_id=program_id)

class ExamEnrollmentForm(forms.ModelForm):
    class Meta:
        model = ExamEnrollment
        fields = ['exam_record', 'batch', 'semester']
        widgets = {
            'exam_record': forms.Select(attrs={'class': 'form-control'}),
            'batch': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            if user.role == 'Admin':
                self.fields['exam_record'].queryset = ExamRecord.objects.all()
                self.fields['batch'].queryset = Batch.objects.all()
                self.fields['semester'].queryset = Semester.objects.all()
            elif user.role == 'Faculty':
                self.fields['exam_record'].queryset = ExamRecord.objects.filter(program__in=user.department.programs.all())
                self.fields['batch'].queryset = Batch.objects.filter(program__in=user.department.programs.all())
                program_id = self.initial.get('program') or self.data.get('program')
                if program_id:
                    self.fields['semester'].queryset = Semester.objects.filter(program_id=program_id)