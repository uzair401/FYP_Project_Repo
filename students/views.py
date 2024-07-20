from django.shortcuts import render
from .models import Student
# Create your views here.

def student(request, course_id):
    # Query students who are enrolled in the given course_id
    students = Student.objects.filter(enrollments__course_id=course_id)
    return render(request, 'students/students.html', {'students': students})