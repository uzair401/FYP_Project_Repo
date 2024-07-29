from django import forms
from .models import Department, Program, Semester, Course, Batch

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        widgets = {
            'department_name': forms.TextInput(attrs={'class': 'form-control'}),
            'department_discipline': forms.TextInput(attrs={'class': 'form-control'}),
            'department_description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = '__all__'
        widgets = {
            'program_name': forms.TextInput(attrs={'class': 'form-control'}),
            'program_code': forms.TextInput(attrs={'class': 'form-control'}),
            'number_of_semesters': forms.NumberInput(attrs={'class': 'form-control'}),
            'program_description': forms.Textarea(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
        }

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = '__all__'
        widgets = {
            'semester_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'semester_category': forms.TextInput(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={'class': 'form-control'}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control'}),
            'course_code': forms.TextInput(attrs={'class': 'form-control'}),
            'credit_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'internal_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'mid_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'final_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'course_description': forms.Textarea(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
        }

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = '__all__'
        widgets = {
            'batch_name': forms.TextInput(attrs={'class': 'form-control'}),
            'batch_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'batch_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'batch_session': forms.TextInput(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={'class': 'form-control'}),
        }