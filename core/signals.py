from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import User
from academics.models import Program, Semester

@receiver(post_save, sender=Program)
def create_semesters(sender, instance, created, **kwargs):
    if created:
        for i in range(1, instance.number_of_semesters + 1):
            semester_category = 'Fall' if i % 2 == 1 else 'Spring'
            semester, created = Semester.objects.get_or_create(
                semester_number=i, 
                semester_category=semester_category, 
                program=instance
            )

@receiver(post_save, sender=User)
def assign_user_group(sender, instance, created, **kwargs):
    if created:
        # Check and assign groups based on user role
        try:
            if instance.role == 'Admin':
                admin_group, created = Group.objects.get_or_create(name='Admin')
                instance.groups.add(admin_group)
                instance.is_staff = True
                instance.is_superuser = True
            elif instance.role == 'Faculty':
                faculty_group, created = Group.objects.get_or_create(name='Faculty')
                instance.groups.add(faculty_group)
                instance.is_staff = True
                instance.is_superuser = False
            elif instance.role == 'Editor':
                editor_group, created = Group.objects.get_or_create(name='Editor')
                instance.groups.add(editor_group)
                instance.is_staff = False
                instance.is_superuser = False
        except Group.DoesNotExist:
            print(f"Group for role {instance.role} does not exist.")
