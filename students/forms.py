from django import forms
from .models import Student
from academics.models import Department, Program, Batch

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
        user_role = kwargs.pop('user_role', None)
        super().__init__(*args, **kwargs)
        
        if user_role in ['Faculty', 'Editor']:
            # Automatically select the department based on the user's role
            if hasattr(self.instance, 'department') and self.instance.department:
                department_id = self.instance.department.id

        if department_id:
            self.fields['department'].queryset = Department.objects.filter(department_id=department_id)
            self.fields['program'].queryset = Program.objects.filter(department_id=department_id)
            self.fields['batch'].queryset = Batch.objects.filter(program__department__department_id=department_id)
        else:
            self.fields['department'].queryset = Department.objects.none()
            self.fields['program'].queryset = Program.objects.none()
            self.fields['batch'].queryset = Batch.objects.none()
