from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from academics.models import Course, Semester
from students.models import Student, Enrollment

@receiver(post_save, sender=Student)
def assign_courses_to_student(sender, instance, created, **kwargs):
    if created:
        print("Assign courses to student signal triggered!")
        current_semesters = Semester.objects.filter(program=instance.program).order_by('semester_number')
        for semester in current_semesters:
            courses = Course.objects.filter(semester=semester)
            for course in courses:
                Enrollment.objects.get_or_create(
                    student=instance,
                    course=course,
                    semester=semester,
                    defaults={'student': instance, 'course': course, 'semester': semester}
                )

@receiver(post_save, sender=Course)
def assign_course_to_students(sender, instance, created, **kwargs):
    if created:
        print("Assign course to students signal triggered!")
        if instance.semester:
            students = Student.objects.filter(program=instance.semester.program)
            for student in students:
                Enrollment.objects.get_or_create(
                    student=student,
                    course=instance,
                    semester=instance.semester,
                    defaults={'student': student, 'course': instance, 'semester': instance.semester}
                )