from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from academics.models import Course, Semester, Program, Batch  # Import models from the academics app
from students.models import Student, Enrollment  # Import models from the users app

@receiver(post_save, sender=Student)
def assign_courses_to_student(sender, instance, created, **kwargs):
    if created:
        # Automatically assign courses to the newly created student
        courses = Course.objects.filter(semester=instance.semester, program=instance.program, batch=instance.batch)
        for course in courses:
            Enrollment.objects.get_or_create(
                student=instance,
                course=course,
                semester=instance.semester
            )

@receiver(post_save, sender=Course)
def assign_course_to_students(sender, instance, created, **kwargs):
    if created:
        # Automatically assign the new course to all students in the same semester and program
        students = Student.objects.filter(program=instance.program, batch=instance.batch, semester=instance.semester)
        for student in students:
            Enrollment.objects.get_or_create(
                student=student,
                course=instance,
                semester=instance.semester
            )
