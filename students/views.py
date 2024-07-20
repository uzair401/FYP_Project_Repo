from django.shortcuts import render
from .models import Student
# Create your views here.

def student(request, course_id):
    students = Student.objects.filter(enrollment__course_id=course_id)
    return render(request, 'student.html', {'students': students})
