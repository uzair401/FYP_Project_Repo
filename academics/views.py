from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Department, Program, Semester, Course, Batch
from .forms import DepartmentForm, ProgramForm, CourseForm, SemesterForm, BatchForm
from django.contrib.auth.decorators import login_required

@login_required
def department(request):
    departments = Department.objects.all()
    form = DepartmentForm()

    # Create a dictionary of forms for each department
    update_forms = {department.department_id: DepartmentForm(instance=department) for department in departments}

    return render(request, 'academics/departments.html', {
        'departments': departments,
        'form': form,
        'update_forms': update_forms,
    })

@csrf_exempt
@login_required
def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save()
            return JsonResponse({'success': True, 'message': f'{department.department_name} added successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Error adding department: ' + str(form.errors)})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@csrf_exempt
@login_required
def department_update(request, department_id):
    department = get_object_or_404(Department, department_id=department_id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Department updated successfully!'})
        else:
            return JsonResponse({'success': False, 'message': 'Failed to update department.', 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
@login_required
def department_delete(request, department_id):
    department = get_object_or_404(Department, department_id=department_id)
    if request.method == 'POST':
        department.delete()
        return JsonResponse({'success': True, 'message': f'Department {department.department_name} deleted successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

# Program Section 
@login_required
def program(request):
    programs = Program.objects.all()
    form = ProgramForm()

    # Create a dictionary of forms for each program
    update_forms = {program.program_id: ProgramForm(instance=program) for program in programs}

    return render(request, 'academics\program.html', {
        'programs': programs,
        'form': form,
        'update_forms': update_forms,
    })

@csrf_exempt
@login_required
def add_program(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            program = form.save()
            return JsonResponse({'success': True, 'message': f'{program.program_name} added successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Error adding Program: ' + str(form.errors)})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@csrf_exempt
@login_required
def program_update(request, program_id):
    program = get_object_or_404(Program, program_id=program_id)
    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Program updated successfully!'})
        else:
            return JsonResponse({'success': False, 'message': 'Failed to update Program.', 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
@login_required
def program_delete(request, program_id):
    program = get_object_or_404(Program, program_id=program_id)
    if request.method == 'POST':
        program.delete()
        return JsonResponse({'success': True, 'message': f'Department {program.program_name} deleted successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

# Semester Section
@login_required
def semester(request):
    semesters = Semester.objects.all()
    form = SemesterForm()

    # Create a dictionary of forms for each department
    update_forms = {semester.semester_id: SemesterForm(instance=semester) for semester in semesters}

    return render(request, 'academics\semester.html', {
        'semesters': semesters,
        'form': form,
        'update_forms': update_forms,
    })

@csrf_exempt
@login_required
def add_semester(request):
    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            semester = form.save()
            return JsonResponse({'success': True, 'message': f'{semester.semester_number} added successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Error adding Semester: ' + str(form.errors)})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@csrf_exempt
@login_required
def semester_update(request, semester_id):
    semester = get_object_or_404(Semester, semester_id=semester_id)
    if request.method == 'POST':
        form = SemesterForm(request.POST, instance=semester)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Semester updated successfully!'})
        else:
            return JsonResponse({'success': False, 'message': 'Failed to update Semester.', 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
@login_required
def semester_delete(request, semester_id):
    semester = get_object_or_404(Semester, semester_id=semester_id)
    if request.method == 'POST':
        semester.delete()
        return JsonResponse({'success': True, 'message': f'Semester {semester.semester_number} deleted successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

# Course Section 
@login_required
def course(request):
    courses = Course.objects.all()
    form = CourseForm()

    # Create a dictionary of forms for each department
    update_forms = {course.course_id: CourseForm(instance=course) for course in courses}

    return render(request, 'academics\course.html', {
        'courses': courses,
        'form': form,
        'update_forms': update_forms,
    })

@csrf_exempt
@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            return JsonResponse({'success': True, 'message': f'{course.course_name} added successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Error adding Course: ' + str(form.errors)})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@csrf_exempt
@login_required
def course_update(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Course updated successfully!'})
        else:
            return JsonResponse({'success': False, 'message': 'Failed to update Course.', 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
@login_required
def course_delete(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    if request.method == 'POST':
        course.delete()
        return JsonResponse({'success': True, 'message': f'Course {course.course_name} deleted successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

# Batch Section
@login_required
def batch(request):
    batches = Batch.objects.all()
    form = BatchForm()

    # Create a dictionary of forms for each department
    update_forms = {batch.batch_id: BatchForm(instance=batch) for batch in batches}

    return render(request, 'academics\programs_batches.html', {
        'batches': batches,
        'form': form,
        'update_forms': update_forms,
    })

@csrf_exempt
@login_required
def add_batch(request):
    if request.method == 'POST':
        form = BatchForm(request.POST)
        if form.is_valid():
            batch = form.save()
            return JsonResponse({'success': True, 'message': f'{batch.batch_name} added successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Error adding Batch: ' + str(form.errors)})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@csrf_exempt
@login_required
def batch_update(request, batch_id):
    batch = get_object_or_404(Batch, batch_id=batch_id)
    if request.method == 'POST':
        form = BatchForm(request.POST, instance=batch)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Batch updated successfully!'})
        else:
            return JsonResponse({'success': False, 'message': 'Failed to update Batch.', 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
@login_required
def batch_delete(request, batch_id):
    batch = get_object_or_404(Batch, batch_id=batch_id)
    if request.method == 'POST':
        batch.delete()
        return JsonResponse({'success': True, 'message': f'Batch {batch.batch_name} deleted successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})