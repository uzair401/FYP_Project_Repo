from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Department
from .forms import DepartmentForm

def department(request):
    departments = Department.objects.all()
    form = DepartmentForm()

    # Create a dictionary of forms for each department
    update_forms = {department.department_id: DepartmentForm(instance=department) for department in departments}

    return render(request, 'academics/departments.html', {
        'departments': departments,
        'form': form,
        'update_forms': update_forms,
    })

@csrf_exempt
def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save()
            return JsonResponse({'success': True, 'message': f'{department.department_name} added successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Error adding department: ' + str(form.errors)})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@csrf_exempt
def department_update(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Department updated successfully!'})
        else:
            return JsonResponse({'success': False, 'message': 'Failed to update department.', 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def department_delete(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if request.method == 'POST':
        department.delete()
        return JsonResponse({'success': True, 'message': f'Department {department.department_name} deleted successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})
