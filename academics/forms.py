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
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from the passed arguments
        department_id = kwargs.pop('department_id', None)
        super().__init__(*args, **kwargs)
        if department_id and user and not user.is_superuser:
            self.fields['department'].queryset = Department.objects.filter(department_id=department_id)

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
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        department_id = kwargs.pop('department_id', None)
        program_id = kwargs.pop('program_id', None)
        super().__init__(*args, **kwargs)
        if user and not user.is_superuser:
            if department_id:
                self.fields['program'].queryset = Program.objects.filter(department__department_id=department_id)
            elif program_id:
                self.fields['program'].queryset = Program.objects.filter(program_id=program_id)

    class Meta:
        model = Semester
        fields = '__all__'
        widgets = {
            'semester_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'semester_category': forms.TextInput(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={'class': 'form-control'}),
        }
class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        department_id = kwargs.pop('department_id', None)
        super().__init__(*args, **kwargs)
        if user and not user.is_superuser:
            if department_id:
                self.fields['semester'].queryset = Semester.objects.filter(program__department__department_id=department_id)

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
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        department_id = kwargs.pop('department_id', None)
        super().__init__(*args, **kwargs)
        if user and not user.is_superuser:
            if department_id:
                self.fields['program'].queryset = Program.objects.filter(department__department_id=department_id)
        self.fields['batch_name'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Include Program Code e.g., BCS-20T'})
        self.fields['batch_name'].help_text = '<pclass="small mt-0 style="font-size: 11px;"><strong>Important! Include the Program Code Befor Batch Name to Avoid Confilcts. (BBA-20T, BCS-20T)</p>'
    class Meta:
        model = Batch
        fields = '__all__'
        widgets = {
            'batch_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Include Program Code e.g., BCS-20T'}),
            'batch_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'batch_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'batch_session_start': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control', 
                    'type': 'date', 
                    'placeholder': 'YYYY-MM-DD'
                }
            ),
            'batch_session_end': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control', 
                    'type': 'date', 
                    'placeholder': 'YYYY-MM-DD'
                }
            ),
            'program': forms.Select(attrs={'class': 'form-control'}),
            'batch_status': forms.Select(attrs={'class': 'form-control'}),
        }
