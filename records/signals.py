from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import ExamRecord, ExamEnrollment, Batch, Semester

def get_current_semester_and_number(current_date):
    """Determine the current semester and its number based on the current date."""
    # Determine if the current month is in Spring or Fall semester
    if 9 <= current_date.month <= 12:
        return current_date.year, 'Fall'
    elif 1 <= current_date.month <= 2:
        return current_date.year - 1, 'Fall'  # January and February of the next year belong to the Fall semester of the previous year
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















# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.utils import timezone
# from .models import ExamRecord, ExamEnrollment, Batch

# def update_batch_status():
#     """Update batch status to 'passed out' if session end date plus one month has passed."""
#     current_date = timezone.now().date()
    
#     batches_to_update = Batch.objects.filter(batch_status='active')
#     for batch in batches_to_update:
#         batch_end_date = batch.batch_session_end
#         if batch_end_date and (batch_end_date + timezone.timedelta(days=30)) < current_date:
#             batch.batch_status = 'passed out'
#             batch.save()

# @receiver(post_save, sender=ExamRecord)
# def assign_batches(sender, instance, created, **kwargs):
#     if created:
#         current_date = timezone.now().date()

#         # Determine the active batches for the program specified in the ExamRecord
#         active_batches = Batch.objects.filter(
#             program=instance.program,
#             batch_status='active'
#         )

#         for batch in active_batches:
#             # Create an ExamEnrollment record for each active batch
#             ExamEnrollment.objects.get_or_create(
#                 exam_record=instance,
#                 batch=batch
#             )
# update_batch_status()