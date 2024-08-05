from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from core.decorators import faculty_required
from .models import ExamRecord, ExamEnrollment
from academics.models import Course, Semester
from .forms import ExamRecordForm, ExamEnrollmentForm
from .models import StudentExamRecord, StudentSemesterRecord
from students.models import Enrollment
@login_required
@faculty_required
def exam_dashboard(request):
    if request.user.role == 'Admin':
        exam_records = ExamRecord.objects.all()
        form = ExamRecordForm()  # Form without any filtering
        update_forms = {record.record_id: ExamRecordForm(instance=record) for record in exam_records}
    elif request.user.role == 'Faculty':
        department_id = request.user.department.department_id
        exam_records = ExamRecord.objects.filter(
            program__department_id=department_id
        )
        form = ExamRecordForm(user=request.user, data=request.POST or None)  # Pass department_id to the form
        update_forms = {record.record_id: ExamRecordForm(instance=record, user=request.user) for record in exam_records}
    else:
        exam_records = ExamRecord.objects.none()
        form = ExamRecordForm()  # Provide an empty form or restricted access form
        update_forms = {}

    return render(request, 'records/dashboard.html', {
        'exam_records': exam_records,
        'form': form,
        'update_forms': update_forms,
    })

@login_required
@faculty_required
def add_record(request):
    """
    Handle the form submission for adding a new exam record.
    """
    form = ExamRecordForm(request.POST)

    if form.is_valid():
        form.save()
        return JsonResponse({'success': True, 'message': 'Exam record added successfully!'})
    else:
        return JsonResponse({'success': False, 'message': 'Error adding exam record: ' + str(form.errors)})
@login_required
@faculty_required
def batches(request, exam_record_id):
    if request.user.role == 'Admin':
        batches = ExamEnrollment.objects.filter(exam_record_id=exam_record_id)
        update_forms = {enrollment.id: ExamEnrollmentForm(instance=enrollment) for enrollment in batches}
    elif request.user.role == 'Faculty':
        department_id = request.user.department.department_id
        batches = ExamEnrollment.objects.filter(
            exam_record_id=exam_record_id,
            exam_record__program__department_id=department_id
        )
        update_forms = {enrollment.id: ExamEnrollmentForm(instance=enrollment, user=request.user) for enrollment in batches}
    else:
        batches = ExamEnrollment.objects.none()
        update_forms = {}

    return render(request, 'records/batches.html', {
        'batches': batches,
        'update_forms': update_forms,
    })
@login_required
@faculty_required
def update_batch(request, id):
    enrollment = get_object_or_404(ExamEnrollment, id=id)
    if request.method == 'POST':
        form = ExamEnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Batch updated successfully!'})
        else:
            return JsonResponse({'success': False, 'message': 'Failed to update batch. Errors: ' + str(form.errors)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
@login_required
@faculty_required
def semesters(request, batch_id, exam_record_id):
    semesters = ExamEnrollment.objects.filter(batch_id=batch_id, exam_record_id=exam_record_id)
    
    return render(request, 'records/semesters.html', {
        'semesters': semesters,
    })
@login_required
@faculty_required
def courses(request, semester_id):
    exam_enrollment = get_object_or_404(ExamEnrollment, semester__semester_id=semester_id)
    courses = Course.objects.filter(semester=exam_enrollment.semester)

    return render(request, 'records/courses.html', {
        'courses': courses,
        'semester': exam_enrollment.semester,
    })

@login_required
def course_student_records(request, course_id, semester_id):
    # Retrieve the selected course
    course = get_object_or_404(Course, course_id=course_id)
    
    # Retrieve student exam records and semester records for the specified course and semester
    student_exam_records = StudentExamRecord.objects.filter(course_id=course_id, semester_id=semester_id)
    student_semester_records = StudentSemesterRecord.objects.filter(semester_id=semester_id)
    
    # Prepare data dictionary for template
    student_data = {}
    for exam_record in student_exam_records:
        student = exam_record.student
        student_data[student.student_id] = {
            'student': student,
            'course': course,  # Include course in the student data
            'exam_record': exam_record,
            'semester_record': student_semester_records.filter(student=student).first(),
        }
    
    context = {
        'course': course,
        'student_data': student_data,
    }
    
    return render(request, 'records/records.html', context)