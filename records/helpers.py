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