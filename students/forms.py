# forms.py
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'father_name', 'date_of_birth', 'registration_number', 'enrollment_year', 'status', 'department', 'program', 'batch']
