from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from academics.models import Department
from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse
from django.utils.safestring import mark_safe
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'department', 'role')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        department_id = kwargs.pop('department_id', None)
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.role == 'Admin':
            self.fields['department'].required = False
            self.fields['department'].widget.attrs['readonly'] = True
            self.fields['department'].initial = None
        elif department_id:
            self.fields['department'].initial = department_id
            self.fields['department'].queryset = Department.objects.filter(department_id=department_id)
            self.fields['department'].widget.attrs['readonly'] = True
            

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'department', 'role')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        department_id = kwargs.pop('department_id', None)
        super().__init__(*args, **kwargs)

        # Conditionally handle the 'department' field for admins
        if self.instance and self.instance.role == 'Admin':
            self.fields['department'].required = False
            self.fields['department'].widget.attrs['readonly'] = True
            self.fields['department'].initial = None
        elif department_id:
            self.fields['department'].initial = department_id
            self.fields['department'].queryset = Department.objects.filter(department_id=department_id)
            self.fields['department'].widget.attrs['readonly'] = True

        # Provide a link to change the user's password in the admin panel
        if self.instance and self.instance.pk:  # Ensure the instance is saved and has a primary key
            change_password_url = reverse('admin:auth_user_password_change', args=[self.instance.pk])
            self.fields['password'].help_text = mark_safe(
                f'Passwords are encrypted with Algorithm (pbkdf2_sha256), and cannot be displayed directly to avoid security vulnerabilites.'
                f' for a secure password change click on <a href="{change_password_url}">this form</a>. '
            )