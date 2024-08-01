from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from functools import wraps
from django.shortcuts import get_object_or_404
from academics.models import Department, Program, Batch
from core.models import User
from students.models import Student

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'Admin':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'Admin access required.')
            return HttpResponseRedirect(reverse('core:main_dashboard'))  # Adjust 'core:dashboard' to your actual core:dashboard URL name
    return _wrapped_view

def faculty_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is either Faculty or Admin
        if request.user.role in ['Faculty', 'Admin']:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'Faculty or Admin access required.')
            return HttpResponseRedirect(reverse('core:main_dashboard'))  # Adjust 'core:main_dashboard' to your actual main_dashboard URL name
    return _wrapped_view
def editor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'Editor':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'Editor access required.')
            return HttpResponseRedirect(reverse('core:main_dashboard'))  # Adjust 'core:main_dashboard' to your actual core:main_dashboard URL name
    return _wrapped_view

def can_add_update(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role in ['Admin', 'Faculty']:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'You do not have permission to add or update.')
            return HttpResponseRedirect(reverse('core:main_dashboard'))  # Adjust 'core:main_dashboard' to your actual core:main_dashboard URL name
    return _wrapped_view

def can_delete(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'Admin':
            return view_func(request, *args, **kwargs)
        elif request.user.role == 'Faculty':
            user_to_delete = get_object_or_404(User, pk=kwargs.get('user_id'))
            if user_to_delete.role in ['Admin', 'Faculty']:
                messages.error(request, 'You do not have permission to delete this user.')
                return HttpResponseRedirect(reverse('core:main_dashboard'))  # Adjust 'core:main_dashboard' to your actual core:main_dashboard URL name
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'You do not have permission to delete.')
            return HttpResponseRedirect(reverse('core:main_dashboard'))  # Adjust 'core:main_dashboard' to your actual core:main_dashboard URL name
    return _wrapped_view

def can_view(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role in ['Admin', 'Faculty', 'Editor']:
            user_department_id = request.user.department.department_id if hasattr(request.user, 'department') else None
            if request.user.role == 'Admin':
                students = Student.objects.all()
            elif request.user.role in ['Faculty', 'Editor']:
                departments = Department.objects.filter(department_id=user_department_id)
                programs = Program.objects.filter(department__in=departments)
                batches = Batch.objects.filter(program__in=programs)
                students = Student.objects.filter(batch__in=batches)
            else:
                students = Student.objects.none()
            request.filtered_students = students
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'You do not have permission to view this resource.')
            return HttpResponseRedirect(reverse('core:main_dashboard'))  # Adjust 'core:main_dashboard' to your actual core:main_dashboard URL name
    return _wrapped_view

def can_update(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role in ['Admin', 'Faculty', 'Editor']:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'You do not have permission to update.')
            return HttpResponseRedirect(reverse('core:core:main_dashboard'))  # Adjust 'core:core:main_dashboard' to your actual core:core:main_dashboard URL name
    return _wrapped_view

def is_editor(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'Editor':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'You are not authorized to access this page.')
            return HttpResponseRedirect(reverse('core:main_main_dashboard'))  # Adjust 'core:main_dashboar' to your actual dashboard URL name
    return _wrapped_view