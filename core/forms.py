from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from academics.models import Department

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
        if self.instance and self.instance.role == 'Admin':
            self.fields['department'].required = False
            self.fields['department'].widget.attrs['readonly'] = True
            self.fields['department'].initial = None
        elif department_id:
            self.fields['department'].initial = department_id
            self.fields['department'].queryset = Department.objects.filter(department_id=department_id)
            self.fields['department'].widget.attrs['readonly'] = True
        # if 'password' in self.fields:
        #     del self.fields['password']
        self.fields['role'].help_text = '<span style=" color: #666;">For Change of password for this user, Visit admin panel</span>'