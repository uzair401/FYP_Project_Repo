from django.shortcuts import render, redirect
from academics.models import Department 
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import CustomUserCreationForm, CustomUserChangeForm
User = get_user_model()

@login_required
def users(request):
    users = User.objects.all()
    if request.user.role == 'Faculty':
        users = users.filter(department=request.user.department)
    return render(request, 'core/users.html', {'users': users})


@login_required
def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if request.user.role == 'Faculty':
                user.department = request.user.department
                if user.role == 'Admin':
                    messages.error(request, "Faculty cannot create Admin users.")
                    return JsonResponse({'success': False, 'message': "Faculty cannot create Admin users."})
            user.save()
            messages.success(request, f"User {user.username} was created successfully.")
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/user_form.html', {'form': form})


@login_required
def user_update(request, user_id):
    user = get_object_or_404(User, user_id=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"User {user.username} was updated successfully.")
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'core/user_form.html', {'form': form, 'user': user})

@login_required
def user_delete(request, user_id):
    user = get_object_or_404(User, user_id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, f"User {user.username} was deleted successfully.")
        return JsonResponse({'success': True})
    return render(request, 'core/user_confirm_delete.html', {'user': user})
# Create your views here.
@login_required
def dashboard(request):
    departments = Department.objects.all()
    return render(request, 'core/dashboard.html', {'departments': departments})

@login_required
def Logout(request):
    logout(request)  # Log out the user
    return redirect('login')  # Redirect to the login page


