from academics.models import Course, Semester
from records.models import StudentExamRecord
from students.models import Enrollment
from decimal import Decimal

def validate_marks(obtained_internal, obtained_mid, obtained_final, course_internal, course_mid, course_final, course_total):
    obtained_internal = Decimal(obtained_internal)
    obtained_mid = Decimal(obtained_mid)
    obtained_final = Decimal(obtained_final)
    course_internal = Decimal(course_internal)
    course_mid = Decimal(course_mid)
    course_final = Decimal(course_final)
    course_total = Decimal(course_total)
    
    if obtained_internal < 0 or obtained_mid < 0 or obtained_final < 0:
        return False
    if (obtained_internal <= course_internal and
        obtained_mid <= course_mid and
        obtained_final <= course_final and
        (obtained_internal + obtained_mid + obtained_final) <= course_total):
        return True
    else:
        return False

def calculate_grade_point(marks, total_marks):
    marks = Decimal(marks)
    total_marks = Decimal(total_marks)
    
    if total_marks <= 0:
        return False
    if marks < 0 or marks > total_marks:
        return False
    
    normalized_marks = (marks / total_marks) * 100
    
    if normalized_marks < 10:
        return Decimal('0.00')
    
    if 10 <= normalized_marks < 50:
        return Decimal('0.05') * (normalized_marks - 10)
    
    if 50 <= normalized_marks < 90:
        return Decimal('2.00') + Decimal('0.05') * (normalized_marks - 50)
    
    if normalized_marks >= 90:
        return Decimal('4.00')

    return Decimal('0.00')

def calc_grade(marks, total_marks):
    marks = Decimal(marks)
    total_marks = Decimal(total_marks)
    
    if total_marks <= 0:
        raise ValueError("Total marks should be greater than 0.")
    if marks < 0 or marks > total_marks:
        raise ValueError("Marks should be between 0 and total_marks.")
    
    normalized_marks = (marks / total_marks) * 100
    
    if normalized_marks < 50:
        return 'F'
    elif 50 <= normalized_marks < 55:
        return 'C'
    elif 55 <= normalized_marks < 60:
        return 'C'
    elif 60 <= normalized_marks < 65:
        return 'C+'
    elif 65 <= normalized_marks < 70:
        return 'B'
    elif 70 <= normalized_marks < 75:
        return 'B'
    elif 75 <= normalized_marks < 80:
        return 'B+'
    elif 80 <= normalized_marks < 85:
        return 'A'
    elif 85 <= normalized_marks < 90:
        return 'A'
    elif normalized_marks >= 90:
        return 'A+'

    return 'F'

def check_pass_status(obtained_marks, total_marks, passing_marks=50):
    obtained_marks = Decimal(obtained_marks)
    total_marks = Decimal(total_marks)
    
    if total_marks <= 0:
        raise ValueError("Total marks should be greater than 0.")
    if obtained_marks < 0 or obtained_marks > total_marks:
        raise ValueError("Obtained marks should be between 0 and total_marks.")
    
    normalized_marks = (obtained_marks / total_marks) * 100

    if normalized_marks < passing_marks:
        return 'Failed'
    return False

def calculate_semester_gpa(student_id, semester_id):
    courses = Course.objects.filter(enrollment__student_id=student_id, semester_id=semester_id)

    total_credit_hours = Decimal('0.00')
    weighted_grade_points_sum = Decimal('0.00')
    total_course_marks = Decimal('0.00')
    total_obtained_marks = Decimal('0.00')

    for course in courses:
        exam_record = StudentExamRecord.objects.filter(
            student_id=student_id, 
            semester_id=semester_id, 
            course_id=course.course_id
        ).first()
        
        if exam_record:
            gpa_per_course = Decimal(exam_record.gpa_per_course)
            weighted_grade_points = Decimal(course.credit_hours) * gpa_per_course
            weighted_grade_points_sum += weighted_grade_points

            total_obtained_marks += Decimal(exam_record.total_marks)
        else:
            weighted_grade_points = Decimal('0.00')
        
        total_credit_hours += Decimal(course.credit_hours)
        total_course_marks += Decimal(course.total_marks)

    if total_credit_hours == Decimal('0.00'):
        semester_gpa = Decimal('0.00') 
    else:
        semester_gpa = weighted_grade_points_sum / total_credit_hours

    if total_course_marks == Decimal('0.00'):
        percentage = Decimal('0.00')  
    else:
        percentage = (total_obtained_marks / total_course_marks) * Decimal('100.00')

    return {
        'semester_gpa': float(semester_gpa),
        'total_course_marks': float(total_course_marks),
        'total_obtained_marks': float(total_obtained_marks),
        'weighted_grade_points_sum': float(weighted_grade_points_sum),
        'total_credit_hours': float(total_credit_hours),
        'percentage': float(percentage)
    }

def calculate_cgpa(student_id, current_semester_id):
    enrollments = Enrollment.objects.filter(student_id=student_id)
    
    semester_ids = enrollments.values_list('semester_id', flat=True).distinct()
    current_semester = Semester.objects.get(semester_id=current_semester_id)
    relevant_semester_ids = [semester_id for semester_id in semester_ids if semester_id <= current_semester_id]

    total_credit_hours = Decimal('0.00')
    weighted_grade_points_sum = Decimal('0.00')
    
    semesters = Semester.objects.filter(semester_id__in=relevant_semester_ids).order_by('semester_number')
    
    for semester in semesters:
        courses = Course.objects.filter(semester=semester)
        
        for course in courses:
            exam_record = StudentExamRecord.objects.filter(
                student_id=student_id, 
                semester=semester,  
                course=course  
            ).first()
            
            if exam_record:
                gpa_per_course = Decimal(exam_record.gpa_per_course)
                weighted_grade_points = Decimal(course.credit_hours) * gpa_per_course
                weighted_grade_points_sum += weighted_grade_points
                
                total_credit_hours += Decimal(course.credit_hours)
    
    if total_credit_hours == Decimal('0.00'):
        cgpa = Decimal('0.00')  # Handle division by zero scenario
    else:
        cgpa = weighted_grade_points_sum / total_credit_hours
    
    cgpa = Decimal(int(cgpa * 100)) / Decimal('100.00')
    
    return float(cgpa)

def check_current_semester_status(student_id, semester_id):
    failed_courses = []

    exam_records = StudentExamRecord.objects.filter(student_id=student_id, semester_id=semester_id)
    
    for exam_record in exam_records:
        course = exam_record.course
        
        total_marks_obtained = Decimal(exam_record.total_marks)
        if check_pass_status(total_marks_obtained, course.total_marks) == 'Failed':
            failed_courses.append(course.course_code)
            continue  
        
        if exam_record.remarks == 'Failed':
            failed_courses.append(course.course_code)

    return failed_courses

