from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import ExamRecord, ExamEnrollment, StudentExamRecord, StudentSemesterRecord
from academics.models import Semester, Course, Batch
from students.models import Enrollment

def get_current_semester_and_number(current_date):
    """Determine the current semester and its number based on the current date."""
    if 9 <= current_date.month <= 12:
        return current_date.year, 'Fall'
    elif 1 <= current_date.month <= 2:
        return current_date.year - 1, 'Fall'
    elif 3 <= current_date.month <= 8:
        return current_date.year, 'Spring'
    return None, None

def get_semester_number_for_date(batch_start_date, exam_date):
    """Calculate the semester number for a given date based on the batch's start date."""
    semesters_per_year = 2  # Assuming 2 semesters per year
    batch_start_year = batch_start_date.year
    batch_start_month = batch_start_date.month

    year_diff = exam_date.year - batch_start_year
    month_diff = exam_date.month - batch_start_month
    total_months = year_diff * 12 + month_diff

    # Calculate the semester number
    return (total_months // 6) + 1

@receiver(post_save, sender=ExamRecord)
def assign_batches_and_semesters(sender, instance, created, **kwargs):
    if created:
        current_date = timezone.now()
        current_year, semester_season = get_current_semester_and_number(current_date)

        # Determine the active batches for the program specified in the ExamRecord
        active_batches = Batch.objects.filter(
            program=instance.program,
            batch_status='active'
        )

        for batch in active_batches:
            # Skip batches that have passed out
            if batch.batch_session_end < current_date.date():
                continue

            # Calculate the semester number for the batch at the time of the exam
            semester_number = get_semester_number_for_date(batch.batch_session_start, current_date)

            # Fetch the appropriate semester for the given program and semester number
            semester = Semester.objects.filter(
                program=instance.program,
                semester_number=semester_number
            ).first()

            if semester:
                # Create an ExamEnrollment record for each batch and semester
                ExamEnrollment.objects.get_or_create(
                    exam_record=instance,
                    batch=batch,
                    semester=semester
                )

@receiver(post_save, sender=ExamRecord)
def create_student_exam_records(sender, instance, created, **kwargs):
    if created:
        current_date = timezone.now().date()

        # Fetch active batches for the program
        active_batches = Batch.objects.filter(
            program=instance.program,
            batch_status='active'
        )

        for batch in active_batches:
            # Skip batches that have passed out
            if batch.batch_session_end < current_date:
                continue

            # Determine the current semester based on the exam date and batch start date
            semester_number = get_semester_number_for_date(batch.batch_session_start, current_date)
            semester = Semester.objects.filter(
                program=instance.program,
                semester_number=semester_number
            ).first()

            if semester:
                # Fetch all courses for the semester
                courses = Course.objects.filter(semester=semester)

                # Fetch students enrolled in the courses for the batch
                for course in courses:
                    enrollments = Enrollment.objects.filter(course=course, semester=semester, student__batch=batch)

                    for enrollment in enrollments:
                        student = enrollment.student

                        # Create StudentExamRecord
                        student_exam_record, created = StudentExamRecord.objects.get_or_create(
                            exam_record=instance,
                            program=instance.program,
                            semester=semester,
                            course=course,
                            student=student,
                            defaults={
                                'internal_marks': 0,
                                'mid_marks': 0,
                                'final_marks': 0,
                                'percentage_per_course': 0,
                                'gpa_per_course': 0,
                                'remarks': ''
                            }
                        )

@receiver(post_save, sender=ExamRecord)
def create_student_semester_records(sender, instance, created, **kwargs):
    if created:
        current_date = timezone.now().date()

        # Fetch active batches for the program
        active_batches = Batch.objects.filter(
            program=instance.program,
            batch_status='active'
        )

        for batch in active_batches:
            # Skip batches that have passed out
            if batch.batch_session_end < current_date:
                continue

            # Determine the current semester based on the exam date and batch start date
            semester_number = get_semester_number_for_date(batch.batch_session_start, current_date)
            semester = Semester.objects.filter(
                program=instance.program,
                semester_number=semester_number
            ).first()

            if semester:
                # Fetch all courses for the semester
                courses = Course.objects.filter(semester=semester)

                # Fetch students enrolled in the courses for the batch
                for course in courses:
                    enrollments = Enrollment.objects.filter(course=course, semester=semester, student__batch=batch)

                    for enrollment in enrollments:
                        student = enrollment.student

                        # Create StudentExamRecord first
                        student_exam_record, created = StudentExamRecord.objects.get_or_create(
                            exam_record=instance,
                            program=instance.program,
                            semester=semester,
                            course=course,
                            student=student,
                            defaults={
                                'internal_marks': 0,
                                'mid_marks': 0,
                                'final_marks': 0,
                                'percentage_per_course': 0,
                                'gpa_per_course': 0,
                                'remarks': ''
                            }
                        )

                        # Use the created StudentExamRecord to create StudentSemesterRecord
                        StudentSemesterRecord.objects.get_or_create(
                            exam_record=instance,
                            semester=semester,
                            student=student,
                            student_exam_rec=student_exam_record,
                            defaults={
                                'total_semester_marks': 0,
                                'semester_obtained_marks': 0,
                                'percentage': 0,
                                'gpa_per_semester': 0,
                                'cgpa': 0,
                                'remarks': ''
                            }
                        )
