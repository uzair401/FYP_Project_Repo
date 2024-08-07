from academics.models import Course, Semester
from records.models import StudentExamRecord
from students.models import Enrollment

from decimal import Decimal


def validate_marks(obtained_internal, obtained_mid, obtained_final, course_internal, course_mid, course_final, course_total):
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
    if total_marks <= 0:
        return False
    if marks < 0 or marks > total_marks:
        return False
    
    # Normalize marks to a 100-point scale
    normalized_marks = (marks / total_marks) * 100
    
    if normalized_marks < 10:
        return 0.00
    
    if 10 <= normalized_marks < 50:
        # Calculate grade point for normalized marks between 10 and 49
        return 0.05 * (normalized_marks - 10)
    
    if 50 <= normalized_marks < 90:
        # Calculate grade point for normalized marks between 50 and 89
        return 2.00 + 0.05 * (normalized_marks - 50)
    
    if normalized_marks >= 90:
        return 4.00

    # Default case (should not reach here)
    return 0.00

def calc_grade(marks, total_marks):
    if total_marks <= 0:
        raise ValueError("Total marks should be greater than 0.")
    if marks < 0 or marks > total_marks:
        raise ValueError("Marks should be between 0 and total_marks.")
    
    # Normalize marks to a 100-point scale
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

    # Default case (should not reach here)
    return 'F'

def check_pass_status(obtained_marks, total_marks, passing_marks=50):

    if total_marks <= 0:
        raise ValueError("Total marks should be greater than 0.")
    if obtained_marks < 0 or obtained_marks > total_marks:
        raise ValueError("Obtained marks should be between 0 and total_marks.")
    normalized_marks = (obtained_marks / total_marks) * 100

    if normalized_marks < passing_marks:
        return 'Failed'
    return False

# records/helpers.py

def calculate_semester_gpa(student_id, semester_id):
    """
    Calculate the GPA for a given student and semester, including the total marks and obtained marks.
    
    Args:
        student_id (int): The ID of the student.
        semester_id (int): The ID of the semester.
    
    Returns:
        dict: A dictionary containing the semester GPA, total course marks, total obtained marks,
              weighted grade points sum, total credit hours, and percentage.
    """
    # Fetch all courses taken by the student in the semester
    courses = Course.objects.filter(enrollment__student_id=student_id, semester_id=semester_id)

    total_credit_hours = 0
    weighted_grade_points_sum = 0.0
    total_course_marks = 0.0
    total_obtained_marks = 0.0

    for course in courses:
        # Fetch the StudentExamRecord for the current course
        exam_record = StudentExamRecord.objects.filter(
            student_id=student_id, 
            semester_id=semester_id, 
            course_id=course.course_id
        ).first()
        
        if exam_record:
            gpa_per_course = exam_record.gpa_per_course
            weighted_grade_points = float(course.credit_hours) * float(gpa_per_course)
            weighted_grade_points_sum += weighted_grade_points

            total_obtained_marks += float(exam_record.total_marks)
        else:
            # If there's no exam record, treat the GPA as 0 for that course
            weighted_grade_points = 0.0
        
        total_credit_hours += course.credit_hours
        total_course_marks += float(course.total_marks)

    if total_credit_hours == 0:
        semester_gpa = 0.0  # Handle division by zero scenario if no courses or credit hours are zero
    else:
        semester_gpa = weighted_grade_points_sum / total_credit_hours

    if total_course_marks == 0:
        percentage = 0.0  # Handle division by zero scenario if total course marks are zero
    else:
        percentage = (total_obtained_marks / total_course_marks) * 100

    return {
        'semester_gpa': semester_gpa,
        'total_course_marks': total_course_marks,
        'total_obtained_marks': total_obtained_marks,
        'weighted_grade_points_sum': weighted_grade_points_sum,
        'total_credit_hours': total_credit_hours,
        'percentage': percentage
    }

# records/helpers.py



def calculate_cgpa(student_id):
    """
    Calculate the CGPA for a given student based on their performance across all semesters.
    
    Args:
        student_id (int): The ID of the student.
    
    Returns:
        float: The CGPA of the student, truncated to 2 decimal places.
    """
    # Get all enrollments for the student
    enrollments = Enrollment.objects.filter(student_id=student_id)
    
    # Extract semester IDs from these enrollments
    semester_ids = enrollments.values_list('semester_id', flat=True).distinct()
    
    total_credit_hours = Decimal('0.00')
    weighted_grade_points_sum = Decimal('0.00')
    
    # Fetch all semesters with these IDs
    semesters = Semester.objects.filter(semester_id__in=semester_ids)
    
    for semester in semesters:
        # Fetch all courses for the current semester
        courses = Course.objects.filter(semester=semester)
        
        for course in courses:
            # Fetch the StudentExamRecord for the current course
            exam_record = StudentExamRecord.objects.filter(
                student_id=student_id, 
                semester=semester,  
                course=course  
            ).first()
            
            if exam_record:
                # Calculate GPA per course
                gpa_per_course = Decimal(exam_record.gpa_per_course)
                # Calculate weighted grade points
                weighted_grade_points = Decimal(course.credit_hours) * gpa_per_course
                weighted_grade_points_sum += weighted_grade_points
                
                # Accumulate total credit hours
                total_credit_hours += Decimal(course.credit_hours)
    
    if total_credit_hours == Decimal('0.00'):
        cgpa = Decimal('0.00')  # Handle division by zero scenario
    else:
        cgpa = weighted_grade_points_sum / total_credit_hours
    
    # Truncate CGPA to 2 decimal places without rounding
    cgpa = Decimal(int(cgpa * 100)) / Decimal('100.00')
    
    return float(cgpa)
