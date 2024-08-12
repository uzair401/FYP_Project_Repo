from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Set up groups in the core app'

    def handle(self, *args, **kwargs):
        # Define the permissions for each group
        groups_permissions = {
            'Admin': [
                'add_batch', 'change_batch', 'delete_batch', 'view_batch',
                'add_course', 'change_course', 'delete_course', 'view_course',
                'add_department', 'change_department', 'delete_department', 'view_department',
                'add_program', 'change_program', 'delete_program', 'view_program',
                'add_semester', 'change_semester', 'delete_semester', 'view_semester',
                'add_logentry', 'change_logentry', 'delete_logentry', 'view_logentry',
                'add_group', 'change_group', 'delete_group', 'view_group',
                'add_permission', 'change_permission', 'delete_permission', 'view_permission',
                'add_user', 'change_user', 'delete_user', 'view_user',
                'add_contenttype', 'change_contenttype', 'delete_contenttype', 'view_contenttype',
                'add_examrecord', 'change_examrecord', 'delete_examrecord', 'view_examrecord',
                'add_studentexamrecord', 'change_studentexamrecord', 'delete_studentexamrecord', 'view_studentexamrecord',
                'add_studentsemesterrecord', 'change_studentsemesterrecord', 'delete_studentsemesterrecord', 'view_studentsemesterrecord',
                'add_session', 'change_session', 'delete_session', 'view_session',
                'add_enrollment', 'change_enrollment', 'delete_enrollment', 'view_enrollment',
                'add_student', 'change_student', 'delete_student', 'view_student',
            ],
            'Faculty': [
                'add_batch', 'change_batch', 'view_batch',
                'add_course', 'change_course', 'view_course',
                'change_department', 'view_department',
                'add_program', 'change_program', 'view_program',
                'add_semester', 'change_semester', 'view_semester',
                'add_logentry', 'change_logentry', 'delete_logentry', 'view_logentry',
                'view_permission', 
                'add_user', 'change_user', 'delete_user', 'view_user',
                'add_contenttype', 'change_contenttype', 'delete_contenttype', 'view_contenttype',
                'add_examrecord', 'change_examrecord', 'view_examrecord',
                'add_studentexamrecord', 'change_studentexamrecord', 'view_studentexamrecord',
                'add_studentsemesterrecord', 'change_studentsemesterrecord', 'view_studentsemesterrecord',
                'add_student', 'change_student', 'view_student',
            ],
            'Editor': [
                'add_batch', 'change_batch', 'view_batch',
                'add_course', 'change_course', 'view_course',
                'change_program', 'view_program',
                'add_semester', 'change_semester', 'view_semester',
                'change_examrecord', 'view_examrecord',
                'change_studentexamrecord', 'view_studentexamrecord',
                'change_studentsemesterrecord', 'view_studentsemesterrecord',
                'add_student', 'change_student', 'view_student',
            ],
        }

        for group_name, permissions in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'{group_name} group created.'))
            else:
                self.stdout.write(self.style.SUCCESS(f'{group_name} group already exists.'))

            # Assign permissions to the group
            perms = Permission.objects.filter(codename__in=permissions)
            group.permissions.set(perms)
            self.stdout.write(self.style.SUCCESS(f'Permissions assigned to {group_name} group.'))

