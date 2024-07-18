# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Program, Semester, Course
# from students.models import Student, Enrollment

# @receiver(post_save, sender=Program)
# def create_semesters(sender, instance, created, **kwargs):
#     if created:
#         for i in range(1, instance.number_of_semesters + 1):
#             Semester.objects.create(semester_number=i, semester_category='Fall' if i % 2 == 1 else 'Spring', program=instance)

# @receiver(post_save, sender=Student)
# def assign_all_semesters(sender, instance, created, **kwargs):
#     if created:
#         semesters = Semester.objects.filter(program=instance.program).order_by('semester_number')
#         enrollments = []
#         for semester in semesters:
#             courses = Course.objects.filter(semester=semester)
#             for course in courses:
#                 enrollments.append(Enrollment(student=instance, semester=semester, course=course))
#         Enrollment.objects.bulk_create(enrollments)

# @receiver(post_save, sender=Program)
# def create_semesters_for_program(sender, instance, created, **kwargs):
#     if created:
#         for i in range(1, instance.number_of_semesters + 1):
#             Semester.objects.create(
#                 semester_number=i,
#                 semester_category="Fall" if i % 2 == 1 else "Spring",  # Example logic for category
#                 program=instance
#             )
# academics/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Program, Semester

@receiver(post_save, sender=Program)
def create_semesters_for_program(sender, instance, created, **kwargs):
    if created:
        for i in range(1, instance.number_of_semesters + 1):
            Semester.objects.create(
                semester_number=i,
                semester_category="Fall" if i % 2 == 1 else "Spring",  # Example logic for category
                program=instance
            )
