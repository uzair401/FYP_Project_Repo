from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Student
from .forms import StudentForm
from core.decorators import can_view, can_add_update, can_delete

@login_required
@can_view
def student(request):
    # Retrieve the user role and department ID if available
    user_role = request.user.role
    user_department_id = request.user.department.department_id if hasattr(request.user, 'department') else None

    # Filter students based on user role and department
    if user_role == 'Admin':
        students = Student.objects.all()
    elif user_role in ['Faculty', 'Editor']:
        # Filter students based on the department of the program
        students = Student.objects.filter(department_id=user_department_id)
    else:
        students = Student.objects.none()

    # Create forms for adding and updating students
    form = StudentForm()
    update_forms = {student.student_id: StudentForm(instance=student) for student in students}

    # Context to pass to the template
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
def student_delete(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)

    # Check if the logged-in user has permission to delete this student
    if request.user.role not in ['Admin', 'Faculty', 'Editor']:
        return JsonResponse({'success': False, 'message': 'You do not have permission to delete students.'})

    if request.method == 'POST':
        student.delete()
        return JsonResponse({'success': True, 'message': f'Student {student.first_name} {student.last_name} deleted successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})
