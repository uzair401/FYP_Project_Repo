from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Set up groups in the core app'

    def handle(self, *args, **kwargs):
        # Create Admin Group (all permissions)
        admin_group, created = Group.objects.get_or_create(name='Admin')
        if created:
            # Assign all permissions to Admin group
            admin_group.permissions.set(Permission.objects.all())
            self.stdout.write(self.style.SUCCESS('Admin group created and all permissions assigned.'))
        else:
            self.stdout.write(self.style.SUCCESS('Admin group already exists.'))

        # Create Faculty Group (no permissions)
        faculty_group, created = Group.objects.get_or_create(name='Faculty')
        if created:
            self.stdout.write(self.style.SUCCESS('Faculty group created with no permissions.'))
        else:
            self.stdout.write(self.style.SUCCESS('Faculty group already exists.'))

        # Create Editor Group (no permissions)
        editor_group, created = Group.objects.get_or_create(name='Editor')
        if created:
            self.stdout.write(self.style.SUCCESS('Editor group created with no permissions.'))
        else:
            self.stdout.write(self.style.SUCCESS('Editor group already exists.'))
