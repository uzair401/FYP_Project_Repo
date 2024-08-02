from django.db.models.signals import post_save, post_delete
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
@receiver(post_save, sender=Semester)
def update_number_of_semesters(sender, instance, created, **kwargs):
    if created:
        program = instance.program
        program.number_of_semesters = Semester.objects.filter(program=program).count()
        program.save()

@receiver(post_delete, sender=Semester)
def update_number_of_semesters_on_delete(sender, instance, **kwargs):
    program = instance.program
    program.number_of_semesters = Semester.objects.filter(program=program).count()
    program.save()