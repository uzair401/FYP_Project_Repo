from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from core.decorators import faculty_required
from .models import ExamRecord, ExamEnrollment
from academics.models import Course, Semester, Batch
from .forms import ExamRecordForm, ExamEnrollmentForm
from .models import StudentExamRecord, StudentSemesterRecord
from students.models import Enrollment, Student
from . import helpers
from django.core.cache import cache
from django.utils.dateparse import parse_date

def dash(request):
    return render(request, 'records/dash.html')

@login_required
def exam_dashboard(request):
    if request.user.role == 'Admin':
        exam_records = ExamRecord.objects.all()
        form = ExamRecordForm()  # Form without any filtering
        update_forms = {record.record_id: ExamRecordForm(instance=record) for record in exam_records}
    elif request.user.role in ['Faculty','Editor']:
        department_id = request.user.department.department_id
        exam_records = ExamRecord.objects.filter(program__department_id=department_id)
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
    if request.method == 'POST':
        form = ExamRecordForm(request.POST)

        if form.is_valid():
            exam_record = form.save(commit=False)

            # Define the timeframes for Spring and Fall sessions
            spring_start_date = parse_date(f"{exam_record.record_year}-03-01")
            spring_end_date = parse_date(f"{exam_record.record_year}-08-31")
            fall_start_date = parse_date(f"{exam_record.record_year}-09-01")
            fall_end_date = parse_date(f"{exam_record.record_year + 1}-02-28")  # Consider leap year for February end date

            # Check for existing records based on the session
            if exam_record.session == 'Spring':
                existing_records = ExamRecord.objects.filter(
                    exam_date__range=(spring_start_date, spring_end_date),
                    session='Spring',
                    program=exam_record.program,
                    record_year=exam_record.record_year
                )
            elif exam_record.session == 'Fall':
                existing_records = ExamRecord.objects.filter(
                    exam_date__range=(fall_start_date, fall_end_date),
                    session='Fall',
                    program=exam_record.program,
                    record_year=exam_record.record_year
                )

            if existing_records.exists():
                return JsonResponse({'success': False, 'message': f'Exam record already exists for the {exam_record.session} session of this year within the specified timeframe.'})

            # Save the new exam record if no duplicates are found
            exam_record.save()
            return JsonResponse({'success': True, 'message': 'Exam record added successfully!'})
        else:
            return JsonResponse({'success': False, 'message': 'Error adding exam record: ' + str(form.errors)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@login_required
def batches(request, exam_record_id):
    if request.user.role == 'Admin':
        batches = ExamEnrollment.objects.filter(exam_record_id=exam_record_id)
        update_forms = {enrollment.id: ExamEnrollmentForm(instance=enrollment) for enrollment in batches}
    elif request.user.role in ['Faculty', 'Editor']:
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
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@login_required
def semesters(request, batch_id, exam_record_id):
    semesters = ExamEnrollment.objects.filter(batch_id=batch_id, exam_record_id=exam_record_id)
    
    return render(request, 'records/semesters.html', {
        'semesters': semesters,
    })

@login_required
def courses(request, semester_id, batch_id):
    # Retrieve the semester and batch based on the provided IDs
    semester = get_object_or_404(Semester, semester_id=semester_id)
    batch = get_object_or_404(Batch, batch_id=batch_id)
    
    # Retrieve courses for the specified semester
    courses = Course.objects.filter(semester=semester)
    
    return render(request, 'records/courses.html', {
        'courses': courses,
        'semester': semester,
        'batch': batch,
    })
@login_required
def course_student_records(request, course_id, semester_id, batch_id):
    # Generate a unique cache key
    cache_key = f"course_student_records_{course_id}_{semester_id}_{batch_id}"
    
    # Check if the data is already cached
    context = cache.get(cache_key)
    
    if not context:
        # Retrieve the selected course
        course = get_object_or_404(Course, course_id=course_id)
        
        # Retrieve the semester and batch
        semester = get_object_or_404(Semester, semester_id=semester_id)
        batch = get_object_or_404(Batch, batch_id=batch_id)
        
        # Retrieve student exam records and semester records for the specified course, semester, and batch
        student_exam_records = StudentExamRecord.objects.filter(
            course_id=course_id, 
            semester_id=semester_id,
            student__batch=batch
        )
        
        student_semester_records = StudentSemesterRecord.objects.filter(
            semester_id=semester_id,
            student__batch=batch
        )
        
        # Prepare data dictionary for template
        student_data = {}
        for exam_record in student_exam_records:
            student = exam_record.student
            student_data[student.student_id] = {
                'student': student,
                'course': course,
                'exam_record': exam_record,
                'semester_record': student_semester_records.filter(student=student).first(),
            }
        
        context = {
            'course': course,
            'student_data': student_data,
            'batch': batch,
            'semester': semester,
        }
        
        # Cache the context data for a specified period (e.g., 10 minutes)
        cache.set(cache_key, context, timeout=600)  # Cache for 600 seconds (10 minutes)
    
    return render(request, 'records/records.html', context)

@login_required
def update_student_record(request):
    if request.method == 'POST':
        try:
            student_id = int(request.POST.get('student_id'))
            internal_marks = float(request.POST.get('internal_marks'))
            mid_marks = float(request.POST.get('mid_marks'))
            final_marks = float(request.POST.get('final_marks'))
            course_id = int(request.POST.get('course_id'))
            semester_id = int(request.POST.get('semester_id'))

            # Retrieve the relevant records
            exam_record = get_object_or_404(StudentExamRecord, student_id=student_id, course_id=course_id, semester_id=semester_id)
            course = get_object_or_404(Course, course_id=course_id)

            # Validate marks before updating
            if helpers.validate_marks(internal_marks, mid_marks, final_marks, course.internal_marks, course.mid_marks, course.final_marks, course.total_marks):
                total_marks_obtained = internal_marks + mid_marks + final_marks
                exam_record.internal_marks = internal_marks
                exam_record.mid_marks = mid_marks
                exam_record.final_marks = final_marks
                exam_record.total_marks = total_marks_obtained  # Store the actual obtained marks, not normalized

                # Calculate GPA per course based on the actual obtained marks
                gpa_per_course = helpers.calculate_grade_point(total_marks_obtained, course.total_marks)
                exam_record.gpa_per_course = gpa_per_course

                # Calculate grade based on the actual obtained marks
                grade = helpers.calc_grade(total_marks_obtained, course.total_marks)
                exam_record.grade = grade

                # Check if passed or failed
                pass_status = helpers.check_pass_status(total_marks_obtained, course.total_marks)
                exam_record.remarks = 'Failed' if pass_status == 'Failed' else ''

                exam_record.save()

                # Calculate semester GPA
                gpa_data = helpers.calculate_semester_gpa(student_id, semester_id)

                # Get or create StudentSemesterRecord for the current student and semester
                student_semester_record, created = StudentSemesterRecord.objects.get_or_create(
                    student_id=student_id, 
                    semester_id=semester_id,
                    exam_record=exam_record.exam_record  # Ensure this matches the correct exam record
                )

                # Update StudentSemesterRecord with the calculated values
                student_semester_record.total_semester_marks = gpa_data['total_course_marks']
                student_semester_record.semester_obtained_marks = gpa_data['total_obtained_marks']
                student_semester_record.gpa_per_semester = gpa_data['semester_gpa']
                student_semester_record.percentage = gpa_data['percentage']

                # Check current semester status for failed courses
                failed_courses = helpers.check_current_semester_status(student_id, semester_id)
                
                if failed_courses:
                    # If there are failed courses, concatenate their course codes with comma separation
                    student_semester_record.remarks = ', '.join(failed_courses)
                else:
                    student_semester_record.remarks = ''

                student_semester_record.save()

                # Calculate and update CGPA
                cgpa = helpers.calculate_cgpa(student_id, semester_id)
                student_semester_record.cgpa = cgpa
                student_semester_record.save()

                return JsonResponse({'success': True, 'message': 'Record updated successfully!'})
            else:
                return JsonResponse({'success': False, 'message': 'Entered marks are greater than course marks!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)
@login_required
@faculty_required
def reset_student_record(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        course_id = request.POST.get('course_id')
        semester_id = request.POST.get('semester_id')

        exam_record = get_object_or_404(StudentExamRecord, student_id=student_id, course_id=course_id, semester_id=semester_id)

        # Reset marks to 0
        exam_record.internal_marks = 0
        exam_record.mid_marks = 0
        exam_record.final_marks = 0
        exam_record.total_marks = 0
        exam_record.grade = ''
        exam_record.remarks = ''
        exam_record.gpa_per_course = 0.0
        exam_record.save()

        return JsonResponse({'success': True, 'message': 'Record reset successfully!'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})




@login_required
def semesters_rec_dash(request):
    if request.user.role == 'Admin':
        exam_records = ExamRecord.objects.all()
    elif request.user.role in ['Faculty','Editor']:
        department_id = request.user.department.department_id
        exam_records = ExamRecord.objects.filter(program__department_id=department_id)
    else:
        exam_records = ExamRecord.objects.none()

    return render(request, 'records/semesters_records_dash.html', {
        'exam_records': exam_records,
    })

@login_required
def records_batches(request, exam_record_id):
    if request.user.role == 'Admin':
        batches = ExamEnrollment.objects.filter(exam_record_id=exam_record_id)
    elif request.user.role in ['Faculty', 'Editor']:
        department_id = request.user.department.department_id
        batches = ExamEnrollment.objects.filter(
            exam_record_id=exam_record_id,
            exam_record__program__department_id=department_id
        )
    else:
        batches = ExamEnrollment.objects.none()
    return render(request, 'records/batch_results_dash.html', {
        'batches': batches,
    })

@login_required
def records_semester(request, batch_id, exam_record_id):
    semesters = ExamEnrollment.objects.filter(batch_id=batch_id, exam_record_id=exam_record_id)
    
    return render(request, 'records/results_semesters_dash.html', {
        'semesters': semesters,
    })

@login_required
def semester_results(request, semester_id, batch_id, exam_record_id):
    # Generate a unique cache key
    cache_key = f"semester_results_{semester_id}_{batch_id}_{exam_record_id}"
    
    # Check if the data is already cached
    context = cache.get(cache_key)
    
    if not context:
        # Retrieve the semester, batch, and exam record
        semester = get_object_or_404(Semester, semester_id=semester_id)
        batch = get_object_or_404(Batch, batch_id=batch_id)
        exam_record = get_object_or_404(ExamRecord, record_id=exam_record_id)
        
        # Retrieve the courses for the semester
        courses = Course.objects.filter(semester=semester)
        
        # Retrieve students in the batch
        students = Student.objects.filter(batch=batch)
        
        # Initialize context data
        context = {
            'semester': semester,
            'batch': batch,
            'exam_record': exam_record,
            'courses': courses,
            'students': []
        }
        
        for student in students:
            # Retrieve exam and semester records for each student
            student_exam_records = StudentExamRecord.objects.filter(student=student, semester=semester, exam_record=exam_record)
            student_semester_record = get_object_or_404(StudentSemesterRecord, student=student, semester=semester)

            # Prepare data for each student
            student_data = {
                'student': student,
                'courses': {course.course_id: {
                    'course': course,
                    'obtained_marks': 0,
                    'gpa_per_course': 0
                } for course in courses},  # Initialize with default values
                'total_obtained_marks': 0,
                'total_full_marks': 0,
                'percentage': student_semester_record.percentage,
                'gpa_per_semester': student_semester_record.gpa_per_semester,
                'cgpa': student_semester_record.cgpa,
                'remarks': student_semester_record.remarks
            }
            
            for record in student_exam_records:
                course = get_object_or_404(Course, course_id=record.course_id)
                student_data['courses'][course.course_id]['obtained_marks'] = record.total_marks
                student_data['courses'][course.course_id]['gpa_per_course'] = record.gpa_per_course
                student_data['total_obtained_marks'] += record.total_marks
                student_data['total_full_marks'] += course.total_marks
            
            context['students'].append(student_data)
        
        # Cache the context data for a specified period (e.g., 10 minutes)
        cache.set(cache_key, context, timeout=600)  # Cache for 600 seconds (10 minutes)
    
    return render(request, 'records/semester_result.html', context)



# @login_required
# def courses_rec_dash(request):
#     if request.user.role == 'Admin':
#         exam_records = ExamRecord.objects.all()
#     elif request.user.role in ['Faculty','Editor']:
#         department_id = request.user.department.department_id
#         exam_records = ExamRecord.objects.filter(program__department_id=department_id)
#     else:
#         exam_records = ExamRecord.objects.none()

#     return render(request, 'records/semesters_records_dash.html', {
#         'exam_records': exam_records,
#     })

# @login_required
# def course_records_batches(request, exam_record_id):
#     if request.user.role == 'Admin':
#         batches = ExamEnrollment.objects.filter(exam_record_id=exam_record_id)
#     elif request.user.role in ['Faculty', 'Editor']:
#         department_id = request.user.department.department_id
#         batches = ExamEnrollment.objects.filter(
#             exam_record_id=exam_record_id,
#             exam_record__program__department_id=department_id
#         )
#     else:
#         batches = ExamEnrollment.objects.none()
#     return render(request, 'records/batch_results_dash.html', {
#         'batches': batches,
#     })

# @login_required
# def records_semester(request, batch_id, exam_record_id):
#     semesters = ExamEnrollment.objects.filter(batch_id=batch_id, exam_record_id=exam_record_id)
    
#     return render(request, 'records/results_semesters_dash.html', {
#         'semesters': semesters,
#     })



# @login_required
# def semester_results(request, semester_id, batch_id, exam_record_id):
#     # Generate a unique cache key
#     cache_key = f"semester_results_{semester_id}_{batch_id}_{exam_record_id}"
    
#     # Check if the data is already cached
#     context = cache.get(cache_key)
    
#     if not context:
#         # Retrieve the semester, batch, and exam record
#         semester = get_object_or_404(Semester, semester_id=semester_id)
#         batch = get_object_or_404(Batch, batch_id=batch_id)
#         exam_record = get_object_or_404(ExamRecord, record_id=exam_record_id)
        
#         # Retrieve the courses for the semester
#         courses = Course.objects.filter(semester=semester)
        
#         # Retrieve students in the batch
#         students = Student.objects.filter(batch=batch)
        
#         # Initialize context data
#         context = {
#             'semester': semester,
#             'batch': batch,
#             'exam_record': exam_record,
#             'courses': courses,
#             'students': []
#         }
        
#         for student in students:
#             # Retrieve exam and semester records for each student
#             student_exam_records = StudentExamRecord.objects.filter(student=student, semester=semester, exam_record=exam_record)
#             student_semester_record = get_object_or_404(StudentSemesterRecord, student=student, semester=semester)

#             # Prepare data for each student
#             student_data = {
#                 'student': student,
#                 'courses': {course.course_id: {
#                     'course': course,
#                     'obtained_marks': 0,
#                     'gpa_per_course': 0
#                 } for course in courses},  # Initialize with default values
#                 'total_obtained_marks': 0,
#                 'total_full_marks': 0,
#                 'percentage': student_semester_record.percentage,
#                 'gpa_per_semester': student_semester_record.gpa_per_semester,
#                 'cgpa': student_semester_record.cgpa,
#                 'remarks': student_semester_record.remarks
#             }
            
#             for record in student_exam_records:
#                 course = get_object_or_404(Course, course_id=record.course_id)
#                 student_data['courses'][course.course_id]['obtained_marks'] = record.total_marks
#                 student_data['courses'][course.course_id]['gpa_per_course'] = record.gpa_per_course
#                 student_data['total_obtained_marks'] += record.total_marks
#                 student_data['total_full_marks'] += course.total_marks
            
#             context['students'].append(student_data)
        
#         # Cache the context data for a specified period (e.g., 10 minutes)
#         cache.set(cache_key, context, timeout=600)  # Cache for 600 seconds (10 minutes)
    
#     return render(request, 'records/semester_result.html', context)

# @login_required
# def courses(request, semester_id, batch_id):
#     # Retrieve the semester and batch based on the provided IDs
#     semester = get_object_or_404(Semester, semester_id=semester_id)
#     batch = get_object_or_404(Batch, batch_id=batch_id)
    
#     # Retrieve courses for the specified semester
#     courses = Course.objects.filter(semester=semester)
    
#     return render(request, 'records/courses.html', {
#         'courses': courses,
#         'semester': semester,
#         'batch': batch,
#     })