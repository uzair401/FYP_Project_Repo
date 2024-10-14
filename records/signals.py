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
