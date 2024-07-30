from django.db.models.signals import post_save
from django.dispatch import receiver
from academics.models import Program, Semester, Course
from students.models import Student, Enrollment
from django.contrib.auth.models import Group
from django.conf import settings
from .models import User


@receiver(post_save, sender=Program)
def create_semesters(sender, instance, created, **kwargs):
    if created:
        for i in range(1, instance.number_of_semesters + 1):
            Semester.objects.create(semester_number=i, semester_category='Fall' if i % 2 == 1 else 'Spring', program=instance)

@receiver(post_save, sender=Student)
def assign_all_semesters(sender, instance, created, **kwargs):
    if created:
        semesters = Semester.objects.filter(program=instance.program).order_by('semester_number')
        enrollments = []
        for semester in semesters:
            courses = Course.objects.filter(semester=semester)
            for course in courses:
                enrollments.append(Enrollment(student=instance, semester=semester, course=course))
        Enrollment.objects.bulk_create(enrollments)

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import User

@receiver(post_save, sender=User)
def assign_user_group(sender, instance, created, **kwargs):
    if created:
        # Remove any existing groups to avoid duplications or conflicts
        instance.groups.clear()

        # Check and assign groups based on user role
        try:
            if instance.role == 'Admin':
                admin_group = Group.objects.get(name='Admin')
                instance.groups.add(admin_group)
                instance.is_staff = True
                instance.is_superuser = True
            elif instance.role == 'Faculty':
                faculty_group = Group.objects.get(name='Faculty')
                instance.groups.add(faculty_group)
                instance.is_staff = True
                instance.is_superuser = False
            elif instance.role == 'Editor':
                editor_group = Group.objects.get(name='Editor')
                instance.groups.add(editor_group)
                instance.is_staff = False
                instance.is_superuser = False

            # Save the instance to apply changes
            instance.save()
        except Group.DoesNotExist:
            # Handle the case where the group does not exist
            print(f"Group for role {instance.role} does not exist.")
