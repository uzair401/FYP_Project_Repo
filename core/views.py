from django.shortcuts import render, redirect
from academics.models import Department 

# Create your views here.
def dashboard(request):
    departments = Department.objects.all()
    return render(request, 'core/dashboard.html', {'departments': departments})