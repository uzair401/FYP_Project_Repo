from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.
def index(request):
    pass
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('/')