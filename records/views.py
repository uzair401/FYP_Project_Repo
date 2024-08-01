from core.decorators import faculty_required
# Create your views here.
from core.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import ExamRecord
from .forms import ExamRecordForm

@login_required
@faculty_required
def exam_dashboard(request):
    if request.user.role == 'Admin':
        exam_records = ExamRecord.objects.all()
        form = ExamRecordForm()  # Form without any filtering
    elif request.user.role == 'Faculty':
        department_id = request.user.department.department_id
        exam_records = ExamRecord.objects.filter(
            program__department_id=department_id
        )
        form = ExamRecordForm(user=request.user, data=request.POST or None)  # Pass department_id to the form
    else:
        exam_records = ExamRecord.objects.none()
        form = ExamRecordForm()  # Provide an empty form or restricted access form

    update_forms = {record.record_id: ExamRecordForm(instance=record, department_id=request.user.department.department_id) for record in exam_records}

    return render(request, 'records/dashboard.html', {
        'exam_records': exam_records,
        'form': form,
        'update_forms': update_forms,
    })

@login_required
@faculty_required
def add_record(request):
    """
    Handle the form submission for adding a new exam record.
    """
    form = ExamRecordForm(request.POST)

    if form.is_valid():
        form.save()
        return JsonResponse({'success': True, 'message': 'Exam record added successfully!'})
    else:
        return JsonResponse({'success': False, 'message': 'Error adding exam record.' + str(form.errors)})
