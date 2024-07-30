from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.shortcuts import get_object_or_404
from academics.models import  Department, Program, Batch
from core.models import User
from students.models import Student
def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'Admin':
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({'success': False, 'message': 'Admin access required.'}, status=403)
    return _wrapped_view

def faculty_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'Faculty':
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({'success': False, 'message': 'Faculty access required.'}, status=403)
    return _wrapped_view

def editor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'Editor':
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({'success': False, 'message': 'Editor access required.'}, status=403)
    return _wrapped_view

def can_add_update(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role in ['Admin', 'Faculty']:
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({'success': False, 'message': 'You do not have permission to add or update.'}, status=403)
    return _wrapped_view

def can_delete(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'Admin':
            return view_func(request, *args, **kwargs)
        elif request.user.role == 'Faculty':
            # Allow Faculty to delete editors but not other faculty members or admins
            user_to_delete = get_object_or_404(User, pk=kwargs.get('user_id'))
            if user_to_delete.role == 'Admin' or user_to_delete.role == 'Faculty':
                return JsonResponse({'success': False, 'message': 'You do not have permission to delete this user.'}, status=403)
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({'success': False, 'message': 'You do not have permission to delete.'}, status=403)
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
            return JsonResponse({'success': False, 'message': 'You do not have permission to view this resource.'}, status=403)
    return _wrapped_view

def can_update(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role in ['Admin', 'Faculty', 'Editor']:
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({'success': False, 'message': 'You do not have permission to update.'}, status=403)
    return _wrapped_view

# Example usage in your views:
# @admin_required
# def some_admin_view(request):
#     ...

# @faculty_required
# def some_faculty_view(request):
#     ...

# @editor_required
# def some_editor_view(request):
#     ...

# @can_add_update
# def add_or_update_view(request):
#     ...

# @can_delete
# def delete_view(request):
#     ...

# @can_view
# def view_view(request):
#     ...

# @can_update
# def update_view(request):
#     ...
