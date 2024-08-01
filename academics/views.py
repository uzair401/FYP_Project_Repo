from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Department, Program, Semester, Course, Batch
from .forms import DepartmentForm, ProgramForm, CourseForm, SemesterForm, BatchForm
from django.contrib.auth.decorators import login_required
from core.decorators import faculty_required

@login_required
@faculty_required
def department(request):
    if request.user.role == 'Admin':
        departments = Department.objects.all()
    elif request.user.role in ['Faculty', 'Editor']:
        departments = Department.objects.filter(department_id=request.user.department.department_id)
    else:
        departments = Department.objects.none()

    form = DepartmentForm()
    update_forms = {department.department_id: DepartmentForm(instance=department) for department in departments}

    return render(request, 'academics/departments.html', {
        'departments': departments,
        'form': form,
        'update_forms': update_forms,
    })

@csrf_exempt
@login_required
@faculty_required
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
@faculty_required
def department_update(request, department_id):
    department = get_object_or_404(Department, department_id=department_id)
    
    if request.user.role != 'Admin':
        return JsonResponse({'success': False, 'message': 'You do not have permission to update departments.'})

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
@faculty_required
def department_delete(request, department_id):
    department = get_object_or_404(Department, department_id=department_id)
    
    if request.user.role != 'Admin':
        return JsonResponse({'success': False, 'message': 'You do not have permission to delete departments.'})

    if request.method == 'POST':
        department.delete()
        return JsonResponse({'success': True, 'message': f'Department {department.department_name} deleted successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

# Program Section 
@login_required
def program(request):
    if request.user.role == 'Admin':
        programs = Program.objects.all()
        form = ProgramForm()
        update_forms = {program.program_id: ProgramForm(instance=program) for program in programs}

    elif request.user.role in ['Faculty', 'Editor']:
        programs = Program.objects.filter(department_id=request.user.department.department_id)
        form = ProgramForm(department_id=request.user.department.department_id)
    else:
        programs = Program.objects.none()
    update_forms = {program.program_id: ProgramForm(instance=program, department_id=request.user.department.department_id) for program in programs}
    return render(request, 'academics/program.html', {
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
    
    if request.user.role != 'Admin':
        return JsonResponse({'success': False, 'message': 'You do not have permission to update programs.'})

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
@faculty_required
def program_delete(request, program_id):
    program = get_object_or_404(Program, program_id=program_id)
    
    if request.user.role != 'Admin':
        return JsonResponse({'success': False, 'message': 'You do not have permission to delete programs.'})

    if request.method == 'POST':
        program.delete()
        return JsonResponse({'success': True, 'message': f'Program {program.program_name} deleted successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

# Semester Section
@login_required
def semester(request):
    if request.user.role == 'Admin':
        semesters = Semester.objects.all()
        form = SemesterForm()
    elif request.user.role in ['Faculty', 'Editor']:
        # Filter based on the program's department ID
        departments = Department.objects.filter(department_id=request.user.department.department_id)
        programs = Program.objects.filter(department__in=departments)
        semesters = Semester.objects.filter(program__in=programs)
        form = SemesterForm(department_id=request.user.department.department_id)
    else:
        semesters = Semester.objects.none()
    update_forms = {semester.semester_id: SemesterForm(instance=semester, department_id=request.user.department.department_id) for semester in semesters}

    return render(request, 'academics/semester.html', {
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
    
    if request.user.role != 'Admin':
        return JsonResponse({'success': False, 'message': 'You do not have permission to update semesters.'})

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
@faculty_required
def semester_delete(request, semester_id):
    semester = get_object_or_404(Semester, semester_id=semester_id)
    
    if request.user.role != 'Admin':
        return JsonResponse({'success': False, 'message': 'You do not have permission to delete semesters.'})

    if request.method == 'POST':
        semester.delete()
        return JsonResponse({'success': True, 'message': f'Semester {semester.semester_number} deleted successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

# Course Section 
@login_required
def course(request):
    if request.user.role == 'Admin':
        courses = Course.objects.all()
        form = CourseForm()
    elif request.user.role in ['Faculty', 'Editor']:
        # Filter based on the department ID
        departments = Department.objects.filter(department_id=request.user.department.department_id)
        programs = Program.objects.filter(department__in=departments)
        courses = Course.objects.filter(semester__program__in=programs)
        form = CourseForm(department_id=request.user.department.department_id)
    else:
        courses = Course.objects.none()
    update_forms = {course.course_id: CourseForm(instance=course,department_id=request.user.department.department_id) for course in courses}

    return render(request, 'academics/course.html', {
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
    
    if request.user.role != 'Admin':
        return JsonResponse({'success': False, 'message': 'You do not have permission to update courses.'})

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
@faculty_required
def course_delete(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    
    if request.user.role != 'Admin':
        return JsonResponse({'success': False, 'message': 'You do not have permission to delete courses.'})

    if request.method == 'POST':
        course.delete()
        return JsonResponse({'success': True, 'message': f'Course {course.course_name} deleted successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

# Batch Section 
@login_required
def batch(request):
    if request.user.role == 'Admin':
        batches = Batch.objects.all()
        form = BatchForm()
    elif request.user.role in ['Faculty', 'Editor']:
        # Filter based on the department ID
        departments = Department.objects.filter(department_id=request.user.department.department_id)
        programs = Program.objects.filter(department__in=departments)
        batches = Batch.objects.filter(program__in=programs)
        form = BatchForm(department_id=request.user.department.department_id)

    else:
        batches = Batch.objects.none()
    update_forms = {batch.batch_id: BatchForm(instance=batch,department_id=request.user.department.department_id) for batch in batches}

    return render(request, 'academics/programs_batches.html', {
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
    
    if request.user.role != 'Admin':
        return JsonResponse({'success': False, 'message': 'You do not have permission to update batches.'})

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
@faculty_required
def batch_delete(request, batch_id):
    batch = get_object_or_404(Batch, batch_id=batch_id)
    
    if request.user.role != 'Admin':
        return JsonResponse({'success': False, 'message': 'You do not have permission to delete batches.'})

    if request.method == 'POST':
        batch.delete()
        return JsonResponse({'success': True, 'message': f'Batch {batch.batch_name} deleted successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})
