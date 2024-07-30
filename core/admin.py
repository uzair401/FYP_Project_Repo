from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User

class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('username', 'name', 'email', 'department', 'role', 'is_superuser', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'role')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', 'email', 'department', 'role')}),  # Added 'email'
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'email', 'department', 'role', 'password1', 'password2'),  # Added 'email'
        }),
    )

    search_fields = ('username', 'name', 'email')  # Added 'email'
    ordering = ('username',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'Faculty':
            return qs.filter(department=request.user.department)
        return qs

admin.site.register(User, UserAdmin)
