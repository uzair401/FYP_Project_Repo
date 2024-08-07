import math
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .models import ExamRecord, ExamEnrollment, StudentExamRecord, StudentSemesterRecord
from academics.models import Batch, Semester, Course
from students.models import Enrollment

@receiver(post_save, sender=ExamRecord)
def create_exam_enrollments(sender, instance, created, **kwargs):
    if created:
        program = instance.program
        exam_date = instance.exam_date
        session = instance.session
        
        # Get all active batches for the program
        active_batches = Batch.objects.filter(program=program, batch_status='active')

        # Get all semesters for the program that match the session
        semesters = Semester.objects.filter(program=program, semester_category=session)

        for batch in active_batches:
            batch_start_date = batch.batch_session_start
            current_semester = None

            # Iterate through semesters to find the current semester
            for semester in semesters:
                if batch_start_date <= exam_date:
                    elapsed_time_in_months = (exam_date.year - batch_start_date.year) * 12 + (exam_date.month - batch_start_date.month)
                    expected_semester_number = math.ceil(elapsed_time_in_months / 6)
                    if semester.semester_number == expected_semester_number:
                        current_semester = semester
                        break

            if current_semester:
                # Check if the ExamEnrollment record already exists
                enrollment_exists = ExamEnrollment.objects.filter(
                    exam_record=instance,
                    batch=batch,
                    semester=current_semester
                ).exists()

                if not enrollment_exists:
                    ExamEnrollment.objects.create(
                        exam_record=instance,
                        batch=batch,
                        semester=current_semester
                    )

                # Create StudentExamRecord and StudentSemesterRecord
                create_student_records(instance, batch, current_semester)

def create_student_records(exam_record, batch, semester):
    current_date = timezone.now().date()

    # Fetch all courses for the semester
    courses = Course.objects.filter(semester=semester)

    # Fetch students enrolled in the courses for the batch
    for course in courses:
        enrollments = Enrollment.objects.filter(course=course, semester=semester, student__batch=batch)

        for enrollment in enrollments:
            student = enrollment.student

            try:
                # Create StudentExamRecord
                student_exam_record, created = StudentExamRecord.objects.get_or_create(
                    exam_record=exam_record,
                    program=exam_record.program,
                    semester=semester,
                    course=course,
                    student=student,
                    defaults={
                        'internal_marks': 0,
                        'mid_marks': 0,
                        'final_marks': 0,
                        'total_marks': 0,
                        'gpa_per_course': 0,
                        'remarks': ''
                    }
                )

                # Create StudentSemesterRecord
                student_semester_record, created = StudentSemesterRecord.objects.get_or_create(
                    student=student,
                    semester=semester,
                    exam_record=exam_record,
                    defaults={
                        'student_exam_rec': student_exam_record,
                        'total_semester_marks': 0,
                        'semester_obtained_marks': 0,
                        'percentage': 0,
                        'gpa_per_semester': 0,
                        'cgpa': 0,
                        'remarks': ''
                    }
                )
                

            except Exception as e:
                print(f"Error creating student records for student '{student}': {e}")

def update_batch_status():
    current_date = timezone.now().date()

    # Get all active batches
    active_batches = Batch.objects.filter(batch_status='active')
    for batch in active_batches:
        # Check if the current date is more than 1 month past the batch's end date
        if current_date > batch.batch_session_end + timedelta(days=30):
            batch.batch_status = 'passedout'
            batch.save()

# Manually calling the update_batch_status function for testing
update_batch_status()














# working code but there is some filtering issue

# import math
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.exceptions import ObjectDoesNotExist
# from django.utils import timezone
# from datetime import timedelta
# from .models import ExamRecord, ExamEnrollment, StudentExamRecord, StudentSemesterRecord
# from academics.models import Batch, Semester, Course
# from students.models import Enrollment

# @receiver(post_save, sender=ExamRecord)
# def create_exam_enrollments(sender, instance, created, **kwargs):
#     if created:
#         program = instance.program
#         exam_date = instance.exam_date
#         session = instance.session
        
#         # Get all active batches for the program
#         active_batches = Batch.objects.filter(program=program, batch_status='active')
#         # Get all semesters for the program that match the session
#         semesters = Semester.objects.filter(program=program, semester_category=session)
#         for batch in active_batches:
#             batch_start_date = batch.batch_session_start
#             current_semester = None

#             # Iterate through semesters to find the current semester
#             for semester in semesters:
#                 if batch_start_date <= exam_date:
#                     elapsed_time_in_months = (exam_date.year - batch_start_date.year) * 12 + (exam_date.month - batch_start_date.month)
#                     expected_semester_number = math.ceil(elapsed_time_in_months / 6)
#                     if semester.semester_number == expected_semester_number:
#                         current_semester = semester
#                         break

#             if current_semester:
#                 # Check if the ExamEnrollment record already exists
#                 enrollment_exists = ExamEnrollment.objects.filter(
#                     exam_record=instance,
#                     batch=batch,
#                     semester=current_semester
#                 ).exists()

#                 if not enrollment_exists:
#                     ExamEnrollment.objects.create(
#                         exam_record=instance,
#                         batch=batch,
#                         semester=current_semester
#                     )
#                 else:
#                     print("Error Occurred in Signals")

#                 # Create StudentExamRecord and StudentSemesterRecord
#                 create_student_records(instance, batch, current_semester)

# def create_student_records(exam_record, batch, semester):
#     current_date = timezone.now().date()

#     # Fetch all courses for the semester
#     courses = Course.objects.filter(semester=semester)

#     # Fetch students enrolled in the courses for the batch
#     for course in courses:
#         enrollments = Enrollment.objects.filter(course=course, semester=semester, student__batch=batch)

#         for enrollment in enrollments:
#             student = enrollment.student

#             try:
#                 # Create StudentExamRecord
#                 student_exam_record, created = StudentExamRecord.objects.get_or_create(
#                     exam_record=exam_record,
#                     program=exam_record.program,
#                     semester=semester,
#                     course=course,
#                     student=student,
#                     defaults={
#                         'internal_marks': 0,
#                         'mid_marks': 0,
#                         'final_marks': 0,
#                         'total_marks': 0,
#                         'gpa_per_course': 0,
#                         'remarks': ''
#                     }
#                 )
#                 # Create StudentSemesterRecord
#                 StudentSemesterRecord.objects.get_or_create(
#                     exam_record=exam_record,
#                     semester=semester,
#                     student=student,
#                     student_exam_rec=student_exam_record,
#                     defaults={
#                         'total_semester_marks': 0,
#                         'semester_obtained_marks': 0,
#                         'percentage': 0,
#                         'gpa_per_semester': 0,
#                         'cgpa': 0,
#                         'remarks': ''
#                     }
#                 )
#             except Exception as e:
#                 print(f"Error creating student records for student ")

# def update_batch_status():
#     current_date = timezone.now().date()

#     # Get all active batches
#     active_batches = Batch.objects.filter(batch_status='active')

#     for batch in active_batches:
#         # Check if the current date is more than 1 month past the batch's end date
#         if current_date > batch.batch_session_end + timedelta(days=30):
#             batch.batch_status = 'passedout'
#             print('Batch to be converterd to passedout', batch.batch_name)
#             batch.save()

# update_batch_status()
# import math
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.exceptions import ObjectDoesNotExist
# from .models import ExamRecord, ExamEnrollment
# from academics.models import Batch, Semester

# @receiver(post_save, sender=ExamRecord)
# def create_exam_enrollments(sender, instance, created, **kwargs):
#     if created:
#         program = instance.program
#         exam_date = instance.exam_date
#         session = instance.session
        
#         # Get all active batches for the program
#         active_batches = Batch.objects.filter(program=program, batch_status='active')
#         # Get all semesters for the program that match the session
#         semesters = Semester.objects.filter(program=program, semester_category=session)
#         for batch in active_batches:
#             batch_start_date = batch.batch_session_start
#             current_semester = None

#             # Iterate through semesters to find the current semester
#             for semester in semesters:
#                 if batch_start_date <= exam_date:
#                     elapsed_time_in_months = (exam_date.year - batch_start_date.year) * 12 + (exam_date.month - batch_start_date.month)
#                     expected_semester_number = math.ceil(elapsed_time_in_months / 6)
#                     if semester.semester_number == expected_semester_number:
#                         current_semester = semester
#                         break

#             if current_semester:
#                 # Check if the ExamEnrollment record already exists
#                 enrollment_exists = ExamEnrollment.objects.filter(
#                     exam_record=instance,
#                     batch=batch,
#                     semester=current_semester
#                 ).exists()

#                 if not enrollment_exists:
#                     ExamEnrollment.objects.create(
#                         exam_record=instance,
#                         batch=batch,
#                         semester=current_semester
#                     )
#                 else:
#                     print("Error Occured in Siganals")






































































# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.utils import timezone
# from .models import ExamRecord, ExamEnrollment, StudentExamRecord, StudentSemesterRecord
# from academics.models import Semester, Course, Batch
# from students.models import Enrollment

# def get_current_semester_and_number(current_date):
#     """Determine the current semester and its number based on the current date."""
#     if 9 <= current_date.month <= 12:
#         return current_date.year, 'Fall'
#     elif 1 <= current_date.month <= 2:
#         return current_date.year - 1, 'Fall'
#     elif 3 <= current_date.month <= 8:
#         return current_date.year, 'Spring'
#     return None, None

# def get_semester_number_for_date(batch_start_date, exam_date):
#     """Calculate the semester number for a given date based on the batch's start date."""
#     semesters_per_year = 2  # Assuming 2 semesters per year
#     batch_start_year = batch_start_date.year
#     batch_start_month = batch_start_date.month

#     year_diff = exam_date.year - batch_start_year
#     month_diff = exam_date.month - batch_start_month
#     total_months = year_diff * 12 + month_diff

#     # Calculate the semester number
#     return (total_months // 6) + 1

# @receiver(post_save, sender=ExamRecord)
# def assign_batches_and_semesters(sender, instance, created, **kwargs):
#     if created:
#         current_date = timezone.now()
#         current_year, semester_season = get_current_semester_and_number(current_date)

#         # Determine the active batches for the program specified in the ExamRecord
#         active_batches = Batch.objects.filter(
#             program=instance.program,
#             batch_status='active'
#         )

#         for batch in active_batches:
#             # Skip batches that have passed out
#             if batch.batch_session_end < current_date.date():
#                 continue

#             # Calculate the semester number for the batch at the time of the exam
#             semester_number = get_semester_number_for_date(batch.batch_session_start, current_date)

#             # Fetch the appropriate semester for the given program and semester number
#             semester = Semester.objects.filter(
#                 program=instance.program,
#                 semester_number=semester_number
#             ).first()

#             if semester:
#                 # Create an ExamEnrollment record for each batch and semester
#                 ExamEnrollment.objects.get_or_create(
#                     exam_record=instance,
#                     batch=batch,
#                     semester=semester
#                 )

# @receiver(post_save, sender=ExamRecord)
# def create_student_exam_records(sender, instance, created, **kwargs):
#     if created:
#         current_date = timezone.now().date()

#         # Fetch active batches for the program
#         active_batches = Batch.objects.filter(
#             program=instance.program,
#             batch_status='active'
#         )

#         for batch in active_batches:
#             # Skip batches that have passed out
#             if batch.batch_session_end < current_date:
#                 continue

#             # Determine the current semester based on the exam date and batch start date
#             semester_number = get_semester_number_for_date(batch.batch_session_start, current_date)
#             semester = Semester.objects.filter(
#                 program=instance.program,
#                 semester_number=semester_number
#             ).first()

#             if semester:
#                 # Fetch all courses for the semester
#                 courses = Course.objects.filter(semester=semester)

#                 # Fetch students enrolled in the courses for the batch
#                 for course in courses:
#                     enrollments = Enrollment.objects.filter(course=course, semester=semester, student__batch=batch)

#                     for enrollment in enrollments:
#                         student = enrollment.student

#                         # Create StudentExamRecord
#                         student_exam_record, created = StudentExamRecord.objects.get_or_create(
#                             exam_record=instance,
#                             program=instance.program,
#                             semester=semester,
#                             course=course,
#                             student=student,
#                             defaults={
#                                 'internal_marks': 0,
#                                 'mid_marks': 0,
#                                 'final_marks': 0,
#                                 'total_marks': 0,
#                                 'gpa_per_course': 0,
#                                 'remarks': ''
#                             }
#                         )

# @receiver(post_save, sender=ExamRecord)
# def create_student_semester_records(sender, instance, created, **kwargs):
#     if created:
#         current_date = timezone.now().date()

#         # Fetch active batches for the program
#         active_batches = Batch.objects.filter(
#             program=instance.program,
#             batch_status='active'
#         )

#         for batch in active_batches:
#             # Skip batches that have passed out
#             if batch.batch_session_end < current_date:
#                 continue

#             # Determine the current semester based on the exam date and batch start date
#             semester_number = get_semester_number_for_date(batch.batch_session_start, current_date)
#             semester = Semester.objects.filter(
#                 program=instance.program,
#                 semester_number=semester_number
#             ).first()

#             if semester:
#                 # Fetch all courses for the semester
#                 courses = Course.objects.filter(semester=semester)

#                 # Fetch students enrolled in the courses for the batch
#                 for course in courses:
#                     enrollments = Enrollment.objects.filter(course=course, semester=semester, student__batch=batch)

#                     for enrollment in enrollments:
#                         student = enrollment.student

#                         # Create StudentExamRecord first
#                         student_exam_record, created = StudentExamRecord.objects.get_or_create(
#                             exam_record=instance,
#                             program=instance.program,
#                             semester=semester,
#                             course=course,
#                             student=student,
#                             defaults={
#                                 'internal_marks': 0,
#                                 'mid_marks': 0,
#                                 'final_marks': 0,
#                                 'gpa_per_course': 0,
#                                 'remarks': ''
#                             }
#                         )

#                         # Use the created StudentExamRecord to create StudentSemesterRecord
#                         StudentSemesterRecord.objects.get_or_create(
#                             exam_record=instance,
#                             semester=semester,
#                             student=student,
#                             student_exam_rec=student_exam_record,
#                             defaults={
#                                 'total_semester_marks': 0,
#                                 'semester_obtained_marks': 0,
#                                 'percentage': 0,
#                                 'gpa_per_semester': 0,
#                                 'cgpa': 0,
#                                 'remarks': ''
#                             }
#                         )
