from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    department = models.ForeignKey('academics.Department', on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=50, choices=[('Admin', 'Admin'), ('Faculty', 'Faculty'), ('Editor', 'Editor')])
    groups = models.ManyToManyField(
        Group,
        related_name='core_user_set',  # Changed related name to avoid conflict
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='core_user_set',  # Changed related name to avoid conflict
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    class Meta:
        unique_together = ('id',)

    def __str__(self):
        return self.name
