# students/filters.py
import django_filters
from .models import Student

class StudentFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = {
            'first_name': ['icontains'],
            'last_name': ['icontains'],
            'registration_number': ['icontains'],
            'department': ['exact'],
            'program': ['exact'],
            'status': ['exact'],
        }
