# academics/forms.py
from django import forms
from .models import Program, Semester, Course, Batch

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = '__all__'

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = '__all__'

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = '__all__'
