# students/views.py
from django.contrib.admin.sites import site
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import TemplateView
from .models import Student

@method_decorator(staff_member_required, name='dispatch')
class student(TemplateView):
    template_name = 'students/students.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get admin filters for the model
        admin_filters = site._registry[Student].get_list_filter(request=self.request)
        context['admin_filters'] = admin_filters
        context['students'] = Student.objects.all()
        return context


# def student(request, course_id):
#     # Query students who are enrolled in the given course_id
#     students = Student.objects.filter(enrollments__course_id=course_id)
#     return render(request, 'students/students.html', {'students': students})