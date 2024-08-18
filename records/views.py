from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404, HttpResponse
from django.template.loader import render_to_string
from collections import OrderedDict
from django.contrib.auth.decorators import login_required
from core.decorators import faculty_required
from .models import ExamRecord, ExamEnrollment
from academics.models import Course, Semester, Batch ,Program
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
        form = ExamRecordForm() 
        update_forms = {record.record_id: ExamRecordForm(instance=record) for record in exam_records}
    elif request.user.role in ['Faculty','Editor']:
        department_id = request.user.department.department_id
        exam_records = ExamRecord.objects.filter(program__department_id=department_id)
        form = ExamRecordForm(user=request.user, data=request.POST or None)  
        update_forms = {record.record_id: ExamRecordForm(instance=record, user=request.user) for record in exam_records}
    else:
        exam_records = ExamRecord.objects.none()
        form = ExamRecordForm() 
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

            spring_start_date = parse_date(f"{exam_record.exam_date.year}-03-01")
            spring_end_date = parse_date(f"{exam_record.exam_date.year}-08-31")
            if exam_record.exam_date.month in [1, 2]:  # January or February
                fall_start_date = parse_date(f"{exam_record.exam_date.year-1}-09-01")
                fall_end_date = parse_date(f"{exam_record.exam_date.year}-02-28")
            else:  # September to December
                fall_start_date = parse_date(f"{exam_record.exam_date.year}-09-01")
                fall_end_date = parse_date(f"{exam_record.exam_date.year+1}-02-28")

            if exam_record.session == 'Spring':
                existing_records = ExamRecord.objects.filter(
                    exam_date__gte=spring_start_date,
                    exam_date__lte=spring_end_date,
                    session='Spring',
                    program=exam_record.program
                )
            elif exam_record.session == 'Fall':
                existing_records = ExamRecord.objects.filter(
                    exam_date__gte=fall_start_date,
                    exam_date__lte=fall_end_date,
                    session='Fall',
                    program=exam_record.program
                )

            if existing_records.exists():
                return JsonResponse({
                    'success': False, 
                    'message': f'Exam record already exists for the {exam_record.session} session of this semester period for the program {exam_record.program}.'
                })

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
    semester = get_object_or_404(Semester, semester_id=semester_id)
    batch = get_object_or_404(Batch, batch_id=batch_id)
    
    courses = Course.objects.filter(semester=semester)
    
    return render(request, 'records/courses.html', {
        'courses': courses,
        'semester': semester,
        'batch': batch,
    })
@login_required
def course_student_records(request, course_id, semester_id, batch_id):
    course = get_object_or_404(Course, course_id=course_id)
    
    semester = get_object_or_404(Semester, semester_id=semester_id)
    batch = get_object_or_404(Batch, batch_id=batch_id)
    
    student_exam_records = StudentExamRecord.objects.filter(
        course_id=course_id, 
        semester_id=semester_id,
        student__batch=batch
    )
    
    student_semester_records = StudentSemesterRecord.objects.filter(
        semester_id=semester_id,
        student__batch=batch
    )
    
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

            exam_record = get_object_or_404(StudentExamRecord, student_id=student_id, course_id=course_id, semester_id=semester_id)
            course = get_object_or_404(Course, course_id=course_id)

            if helpers.validate_marks(internal_marks, mid_marks, final_marks, course.internal_marks, course.mid_marks, course.final_marks, course.total_marks):
                total_marks_obtained = internal_marks + mid_marks + final_marks
                exam_record.internal_marks = internal_marks
                exam_record.mid_marks = mid_marks
                exam_record.final_marks = final_marks
                exam_record.total_marks = total_marks_obtained  
                gpa_per_course = helpers.calculate_grade_point(total_marks_obtained, course.total_marks)
                exam_record.gpa_per_course = gpa_per_course

                grade = helpers.calc_grade(total_marks_obtained, course.total_marks)
                exam_record.grade = grade

                pass_status = helpers.check_pass_status(total_marks_obtained, course.total_marks)
                exam_record.remarks = 'Failed' if pass_status == 'Failed' else ''
                exam_record.is_repeated = "Yes" if int(request.POST.get('is_repeated')) == 1 else "No"

                exam_record.save()
                gpa_data = helpers.calculate_semester_gpa(student_id, semester_id)

                student_semester_record, created = StudentSemesterRecord.objects.get_or_create(
                    student_id=student_id, 
                    semester_id=semester_id,
                    exam_record=exam_record.exam_record  
                )

                student_semester_record.total_semester_marks = gpa_data['total_course_marks']
                student_semester_record.semester_obtained_marks = gpa_data['total_obtained_marks']
                student_semester_record.gpa_per_semester = gpa_data['semester_gpa']
                student_semester_record.percentage = gpa_data['percentage']

                failed_courses = helpers.check_current_semester_status(student_id, semester_id)
                
                if failed_courses:
                    student_semester_record.remarks = ', '.join(failed_courses)
                else:
                    student_semester_record.remarks = ''

                student_semester_record.save()

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

        exam_record.internal_marks = 0
        exam_record.mid_marks = 0
        exam_record.final_marks = 0
        exam_record.total_marks = 0
        exam_record.grade = ''
        exam_record.remarks = ''
        exam_record.gpa_per_course = 0.0
        exam_record.is_repeated = 'No'
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

    return render(request, 'records/semester/semesters_records_dash.html', {
        'exam_records': exam_records,
    })

@login_required
@faculty_required
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
    return render(request, 'records/semester/batch_results_dash.html', {
        'batches': batches,
    })

@login_required
@faculty_required
def records_semester(request, batch_id, exam_record_id):
    semesters = ExamEnrollment.objects.filter(batch_id=batch_id, exam_record_id=exam_record_id)
    
    return render(request, 'records/semester/results_semesters_dash.html', {
        'semesters': semesters,
    })

@login_required
@faculty_required
def semester_results(request, semester_id, batch_id, exam_record_id):
    cache_key = f"semester_results_{semester_id}_{batch_id}_{exam_record_id}"
    
    context = cache.get(cache_key)
    
    if not context:
        semester = get_object_or_404(Semester, semester_id=semester_id)
        batch = get_object_or_404(Batch, batch_id=batch_id)
        exam_record = get_object_or_404(ExamRecord, record_id=exam_record_id)
        
        courses = Course.objects.filter(semester=semester)
        
        students = Student.objects.filter(batch=batch)
        
        context = {
            'semester': semester,
            'batch': batch,
            'exam_record': exam_record,
            'courses': courses,
            'students': []
        }
        
        for student in students:
            student_exam_records = StudentExamRecord.objects.filter(student=student, semester=semester, exam_record=exam_record)
            student_semester_record = get_object_or_404(StudentSemesterRecord, student=student, semester=semester)

            student_data = {
                'student': student,
                'courses': {course.course_id: {
                    'course': course,
                    'obtained_marks': 0,
                    'gpa_per_course': 0
                } for course in courses},  
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
                student_data['courses'][course.course_id]['remarks'] = record.remarks
                student_data['total_obtained_marks'] += record.total_marks
                student_data['total_full_marks'] += course.total_marks
            
            context['students'].append(student_data)
        
        cache.set(cache_key, context, timeout=10)
    
    return render(request, 'records/semester/semester_result.html', context)


@login_required

def courses_rec_dash(request):
    if request.user.role == 'Admin':
        exam_records = ExamRecord.objects.all()
    elif request.user.role in ['Faculty', 'Editor']:
        department_id = request.user.department.department_id
        exam_records = ExamRecord.objects.filter(program__department_id=department_id)
    else:
        exam_records = ExamRecord.objects.none()

    return render(request, 'records/courses/course_records.html', {
        'exam_records': exam_records,
    })

@login_required
def course_records_batches(request, exam_record_id):
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
        
    return render(request, 'records/courses/courses_batch.html', {
        'batches': batches,
    })

@login_required
def courses_semesters(request, batch_id, exam_record_id):
    semesters = ExamEnrollment.objects.filter(batch_id=batch_id, exam_record_id=exam_record_id)
    
    return render(request, 'records/courses/courses_semesters.html', {
        'semesters': semesters,
    })

@login_required
def courses_record(request, semester_id, batch_id):
    semester = get_object_or_404(Semester, semester_id=semester_id)
    batch = get_object_or_404(Batch, batch_id=batch_id)
    
    courses = Course.objects.filter(semester=semester)
    
    return render(request, 'records/courses/courses_courses.html', {
        'courses': courses,
        'semester': semester,
        'batch': batch,
    })

@login_required
def course_results(request, semester_id, batch_id, course_id):
    cache_key = f"course_results_{semester_id}_{batch_id}_{course_id}"
    context = cache.get(cache_key)
    
    if not context:
        semester = get_object_or_404(Semester, semester_id=semester_id)
        batch = get_object_or_404(Batch, batch_id=batch_id)
        course = get_object_or_404(Course, course_id=course_id)

        exam_record = ExamRecord.objects.filter(
            examenrollment__batch=batch,
            examenrollment__semester=semester
        ).first()

        if not exam_record:
            raise Http404("Exam record not found.")
        
        students = Student.objects.filter(batch=batch)
        
        context = {
            'semester': semester,
            'batch': batch,
            'exam_record': exam_record,
            'course': course,
            'students': []
        }
        
        for student in students:
            student_exam_record = StudentExamRecord.objects.filter(
                student=student,
                semester=semester,
                exam_record=exam_record,
                course=course
            ).first()
            
            student_semester_record = StudentSemesterRecord.objects.filter(student=student, semester=semester).first()
            
            internal_marks = mid_marks = final_marks = total_obtained_marks = total_full_marks = percentage = gpa = remarks = 0

            if student_exam_record:
                internal_marks = student_exam_record.internal_marks
                mid_marks = student_exam_record.mid_marks
                final_marks = student_exam_record.final_marks
                total_obtained_marks = student_exam_record.total_marks
                total_full_marks = course.total_marks
                total_internal_marks = course.internal_marks
                total_mid_marks = course.mid_marks
                total_final_marks = course.final_marks
                percentage = (total_obtained_marks / total_full_marks) * 100 if total_full_marks > 0 else 0
                gpa = student_exam_record.gpa_per_course
                remarks = student_exam_record.remarks
                grade = student_exam_record.grade
            
            context['students'].append({
                'student': student,
                'internal_marks': internal_marks,
                'mid_marks': mid_marks,
                'final_marks': final_marks,
                'total_obtained_marks': total_obtained_marks,
                'total_full_marks': total_full_marks,
                'total_internal_marks': total_internal_marks,
                'total_mid_marks': total_mid_marks,
                'total_final_marks': total_final_marks,
                'percentage': percentage,
                'gpa': gpa,
                'grade': grade,
                'remarks': remarks,
            })
        
        cache.set(cache_key, context, timeout=10)
    
    return render(request, 'records/courses/courses_results.html', context)

@login_required
@faculty_required
def transcript_program_selection(request):
    if request.user.role == 'Admin':
        programs = Program.objects.all()
    elif request.user.role == 'Faculty':
        programs = Program.objects.filter(department_id=request.user.department.department_id)
    else:
        programs = Program.objects.none()
    
    return render(request, 'records/transcript/program_selection.html', {
        'programs': programs,
    })

@login_required
@faculty_required
def transcript_batch(request, program_id):
    batches = Batch.objects.filter(program_id=program_id)
    return render(request, 'records/transcript/batches.html', {
        'batches': batches,
    })

@login_required
@faculty_required
def transcript_student(request, batch_id):
    students = Student.objects.filter(batch_id=batch_id)

    return render(request, 'records/transcript/transcript_students.html', {'students':students})



def student_transcript(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    
    student_records = StudentExamRecord.objects.filter(student=student)
    
    semester_records = StudentSemesterRecord.objects.filter(student=student)
    
    include_semesters = request.GET.getlist('include_semesters', [])
    
    semester_records_dict = {}
    for semester_record in semester_records:
        semester_number = semester_record.semester.semester_number
        
        if include_semesters and str(semester_number) not in include_semesters:
            continue
        
        if semester_number not in semester_records_dict:
            semester_records_dict[semester_number] = {
                'semesternumber': semester_record.semester.semester_number,
                'semester_category': semester_record.semester.semester_category,
                'program': semester_record.exam_record.program.program_name,
                'exam_date': semester_record.exam_record.exam_date,
                'total_semester_marks': semester_record.total_semester_marks,
                'total_obtained_marks': semester_record.semester_obtained_marks,
                'gpa_per_semester': semester_record.gpa_per_semester,
                'cgpa': semester_record.cgpa,
                'courses': {},
                'total_credit_hours': sum(
                    record.course.credit_hours for record in student_records.filter(semester=semester_record.semester)
                ),
                'has_failed_course': any(
                    record.remarks and "Failed" in record.remarks for record in student_records.filter(semester=semester_record.semester)
                )
            }
        
        semester_courses = student_records.filter(semester=semester_record.semester)
        
        for record in semester_courses:
            semester_records_dict[semester_number]['courses'][record.course.course_name] = {
                'course_name': record.course.course_name,
                'course_code': record.course.course_code,
                'credit_hours': record.course.credit_hours,
                'obtained_marks': record.total_marks,
                'is_repeated': record.is_repeated,
                'total_marks': record.course.total_marks,
                'gpa_per_course': record.gpa_per_course,
                'remarks': record.remarks,
            }
    
    sorted_semester_records = OrderedDict(sorted(semester_records_dict.items()))

    context = {
        'student': student,
        'semester_records': sorted_semester_records
    }
    
    return render(request, 'records/transcript/transcript.html', context)

