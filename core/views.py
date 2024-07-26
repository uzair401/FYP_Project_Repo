from django.shortcuts import render, redirect
from academics.models import Department 
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required 
from django.urls import resolve, reverse
from django.utils.text import slugify

# Create your views here.
@login_required
def dashboard(request):
    departments = Department.objects.all()
    return render(request, 'core/dashboard.html', {'departments': departments})

@login_required
def Logout(request):
    logout(request)  # Log out the user
    return redirect('login')  # Redirect to the login page

def breadcrumbs(request):
    url_name = resolve(request.path_info).url_name
    if not url_name:
        return {}

    breadcrumbs = [{'name': 'Dashboard', 'url': reverse('dashboard')}]

    # Split the path into components and create breadcrumb items
    path_components = request.path.strip('/').split('/')
    for i, component in enumerate(path_components):
        name = component.replace('_', ' ').capitalize()
        url = '/' + '/'.join(path_components[:i+1])
        breadcrumbs.append({'name': name, 'url': url})

    # Mark the last breadcrumb item as active
    if breadcrumbs:
        breadcrumbs[-1]['url'] = None

    return {'breadcrumbs': breadcrumbs}