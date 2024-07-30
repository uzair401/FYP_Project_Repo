from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .forms import CustomUserCreationForm, CustomUserChangeForm
from academics.models import Department
from django.contrib.auth import logout

User = get_user_model()

@login_required
def users(request):
    users = User.objects.all()
    if request.user.role == 'Faculty':
        users = users.filter(department=request.user.department)
    form = CustomUserCreationForm()
    update_forms = {user.id: CustomUserChangeForm(instance=user) for user in users}
    return render(request, 'core/users.html', {
        'users': users,
        'form': form,
        'update_forms': update_forms,
    })

@login_required
def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Admin role restriction for Faculty
            if request.user.role == 'Faculty' and user.role == 'Admin':
                return JsonResponse({'success': False, 'message': "Faculty cannot create Admin users."})
            if request.user.role == 'Faculty':
                user.department = request.user.department
            try:
                user.save()
                return JsonResponse({'success': True, 'message': f"User {user.username} was created successfully."})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
        else:
            return JsonResponse({'success': False, 'message': form.errors})
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/users.html', {'form': form})

@login_required
def user_update(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Admin role restriction for Faculty
    if request.user.role == 'Faculty':
        if user.role == 'Admin':
            return JsonResponse({'success': False, 'message': "Faculty cannot update Admin users."})
        if user.role != 'Faculty' and user.department != request.user.department:
            return JsonResponse({'success': False, 'message': "Faculty cannot update users from other departments."})

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': f"User {user.username} was updated successfully."})
        else:
            return JsonResponse({'success': False, 'message': form.errors})
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'core/users.html', {'form': form, 'user': user})

@login_required
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Prevent users from deleting themselves
    if user.id == request.user.id:
        return JsonResponse({'success': False, 'message': "You cannot delete your own account. Ask Admin"})
    
    # Admin role restriction for Faculty
    if request.user.role == 'Faculty':
        if user.role == 'Admin':
            return JsonResponse({'success': False, 'message': "Faculty cannot delete Admin users."})
        if user.role != 'Faculty' and user.department != request.user.department:
            return JsonResponse({'success': False, 'message': "Faculty can only delete users from their own department."})

    if request.method == 'POST':
        user.delete()
        return JsonResponse({'success': True, 'message': f"User {user.username} was deleted successfully."})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required
def dashboard(request):
    departments = Department.objects.all()
    return render(request, 'core/dashboard.html', {'departments': departments})

@login_required
def Logout(request):
    logout(request)
    return redirect('login')
