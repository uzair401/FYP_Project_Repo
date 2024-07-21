# students/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Student, Department, Program, Batch
from .forms import StudentForm

def student(request):
        students = Student.objects.all()
        departments = Department.objects.all()
        programs = Program.objects.all()
        batches = Batch.objects.all()
        form = StudentForm()
        return render(request, 'students/students.html', {
        'students': students,
        'departments': departments,
        'programs': programs,
        'batches': batches,
        'form': form
    })

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            return JsonResponse({'success': True, 'message': f'{student.first_name} added successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Student adding error: ' + str(form.errors)})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

# # students/views.py
# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# from .models import Student, Department, Program, Batch

# def student(request):
#     students = Student.objects.all()
#     departments = Department.objects.all()
#     programs = Program.objects.all()
#     batches = Batch.objects.all()
#     statuses = Student.STUDENT_STATUS_CHOICES  # Get status choices directly from the model
#     return render(request, 'students/students.html', {
#         'students': students,
#         'departments': departments,
#         'programs': programs,
#         'batches': batches,
#         'statuses': statuses  # Pass statuses to the template
#     })

# def add_student(request):
#     if request.method == 'POST':
#         try:
#             student = Student(
#                 first_name=request.POST.get('first_name'),
#                 last_name=request.POST.get('last_name'),
#                 father_name=request.POST.get('father_name'),
#                 date_of_birth=request.POST.get('date_of_birth'),
#                 registration_number = request.POST.get('registration_number', '').upper(),
#                 enrollment_year=request.POST.get('enrollment_year'),
#                 status=request.POST.get('status'),
#                 department_id=request.POST.get('department'),
#                 program_id=request.POST.get('program'),
#                 batch_id=request.POST.get('batch')
#             )
#             student.save()
#             return JsonResponse({'success': True, 'message': f'{student.first_name} added successfully'})
#         except Exception as e:
#             return JsonResponse({'success': False, 'message': 'Student adding error: ' + str(e)})
#     return JsonResponse({'success': False, 'message': 'Invalid request'})
