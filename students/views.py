from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Student
from .forms import StudentForm
from core.decorators import can_view, can_add_update, can_delete
from core.decorators import faculty_required
@login_required
def student(request):
    # Retrieve the user role and department ID if available
    user_department_id = request.user.department.department_id if hasattr(request.user, 'department') else None

    # Filter students based on user role and department
    if request.user.role == 'Admin':
        students = Student.objects.all()
        form = StudentForm()
    elif request.user.role in ['Faculty', 'Editor']:
        students = Student.objects.filter(department_id=user_department_id)
        form = StudentForm(department_id=request.user.department.department_id)
    else:
        students = Student.objects.none()
    update_forms = {
    student.student_id: StudentForm(instance=student, department_id=request.user.department.department_id)
    for student in students
}   # Context to pass to the template
    context = {
        'students': students,
        'form': form,
        'update_forms': update_forms,
    }

    return render(request, 'students/students.html', context)

@csrf_exempt
@login_required
@can_add_update
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            return JsonResponse({'success': True, 'message': f'{student.first_name} added successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Error adding student: ' + str(form.errors)})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@csrf_exempt
@login_required
@can_add_update
def student_update(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)

    # Check if the logged-in user has permission to update this student
    if request.user.role not in ['Admin', 'Faculty', 'Editor']:
        return JsonResponse({'success': False, 'message': 'You do not have permission to update students.'})

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Student updated successfully!'})
        else:
            return JsonResponse({'success': False, 'message': 'Failed to update student.', 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
@login_required
@can_delete
@faculty_required
def student_delete(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)

    # Check if the logged-in user has permission to delete this student
    if request.user.role not in ['Admin', 'Faculty', 'Editor']:
        return JsonResponse({'success': False, 'message': 'You do not have permission to delete students.'})

    if request.method == 'POST':
        student.delete()
        return JsonResponse({'success': True, 'message': f'Student {student.first_name} {student.last_name} deleted successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})
