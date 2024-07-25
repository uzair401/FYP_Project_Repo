from django.shortcuts import render, redirect
from academics.models import Department 
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required 


# Create your views here.
@login_required
def dashboard(request):
    departments = Department.objects.all()
    return render(request, 'core/dashboard.html', {'departments': departments})

@login_required
def Logout(request):
    logout(request)  # Log out the user
    return redirect('login')  # Redirect to the login page