# students/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Student, Department, Program, Batch
from .forms import StudentForm
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import Group


@login_required
def student(request):
    students = Student.objects.all()
    departments = Department.objects.all()
    programs = Program.objects.all()
    batches = Batch.objects.all()
    form = StudentForm()

    # Create a dictionary of forms for each student
    update_forms = {student.student_id: StudentForm(instance=student) for student in students}

    return render(request, 'students/students.html', {
        'students': students,
        'departments': departments,
        'programs': programs,
        'batches': batches,
        'form': form,
        'update_forms': update_forms,
    })

@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            return JsonResponse({'success': True, 'message': f'{student.first_name} added successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Student adding error: ' + str(form.errors)})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def student_update(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Student updated successfully!'})
        else:
            return JsonResponse({'success': False, 'message': 'Failed to update student.', 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
def student_delete(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        student.delete()
        return JsonResponse({'success': True, 'message': f'Student {student.first_name} {student.last_name} deleted successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})
