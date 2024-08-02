# forms.py
from django import forms
from .models import Student
from academics.models import Department, Program,Batch
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'father_name', 'date_of_birth', 'registration_number', 'enrollment_year', 'status', 'department', 'program', 'batch']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control'}),
            'enrollment_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={'class': 'form-control'}),
            'batch': forms.Select(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        department_id = kwargs.pop('department_id', None)
        super().__init__(*args, **kwargs)
        if department_id:
            self.fields['department'].queryset = Department.objects.filter(department_id=department_id)
            self.fields['program'].queryset = Program.objects.filter(department_id=department_id)
            self.fields['batch'].queryset = Batch.objects.filter(program__department__department_id=department_id)
