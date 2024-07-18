from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'name', 'father_name', 'department', 'role')
    search_fields = ('username', 'email', 'name')
    list_filter = ('department', 'role')


