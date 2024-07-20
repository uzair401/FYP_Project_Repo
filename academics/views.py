# academics/views.py
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Department, Program, Semester, Course, Batch
from .forms import ProgramForm, SemesterForm, CourseForm, BatchForm

def program(request, department_id):
    programs = Program.objects.filter(department_id=department_id)
    return render(request, 'academics/program.html', {'programs': programs})

def batch(request, program_id):
    batches = Batch.objects.filter(program_id=program_id)
    return render(request, 'academics/batch.html', {'batches': batches})

def semester(request, program_id):
    semesters = Semester.objects.filter(program_id=program_id)
    return render(request, 'academics/semester.html', {'semesters': semesters})

def course(request, semester_id):
    courses = Course.objects.filter(semester_id=semester_id)
    return render(request, 'academics/course.html', {'courses': courses})
# # Program Views
# class ProgramListView(ListView):
#     model = Program
#     template_name = 'academics/program_list.html'
#     context_object_name = 'programs'

# class ProgramCreateView(CreateView):
#     model = Program
#     form_class = ProgramForm
#     template_name = 'academics/program_form.html'
#     success_url = reverse_lazy('program-list')

# class ProgramUpdateView(UpdateView):
#     model = Program
#     form_class = ProgramForm
#     template_name = 'academics/program_form.html'
#     success_url = reverse_lazy('program-list')

# class ProgramDeleteView(DeleteView):
#     model = Program
#     template_name = 'academics/program_confirm_delete.html'
#     success_url = reverse_lazy('program-list')

# # Semester Views
# class SemesterListView(ListView):
#     model = Semester
#     template_name = 'academics/semester_list.html'
#     context_object_name = 'semesters'

# class SemesterCreateView(CreateView):
#     model = Semester
#     form_class = SemesterForm
#     template_name = 'academics/semester_form.html'
#     success_url = reverse_lazy('semester-list')

# class SemesterUpdateView(UpdateView):
#     model = Semester
#     form_class = SemesterForm
#     template_name = 'academics/semester_form.html'
#     success_url = reverse_lazy('semester-list')

# class SemesterDeleteView(DeleteView):
#     model = Semester
#     template_name = 'academics/semester_confirm_delete.html'
#     success_url = reverse_lazy('semester-list')

# # Course Views
# class CourseListView(ListView):
#     model = Course
#     template_name = 'academics/course_list.html'
#     context_object_name = 'courses'

# class CourseCreateView(CreateView):
#     model = Course
#     form_class = CourseForm
#     template_name = 'academics/course_form.html'
#     success_url = reverse_lazy('course-list')

# class CourseUpdateView(UpdateView):
#     model = Course
#     form_class = CourseForm
#     template_name = 'academics/course_form.html'
#     success_url = reverse_lazy('course-list')

# class CourseDeleteView(DeleteView):
#     model = Course
#     template_name = 'academics/course_confirm_delete.html'
#     success_url = reverse_lazy('course-list')

# # Batch Views
# class BatchListView(ListView):
#     model = Batch
#     template_name = 'academics/batch_list.html'
#     context_object_name = 'batches'

# class BatchCreateView(CreateView):
#     model = Batch
#     form_class = BatchForm
#     template_name = 'academics/batch_form.html'
#     success_url = reverse_lazy('batch-list')

# class BatchUpdateView(UpdateView):
#     model = Batch
#     form_class = BatchForm
#     template_name = 'academics/batch_form.html'
#     success_url = reverse_lazy('batch-list')

# class BatchDeleteView(DeleteView):
#     model = Batch
#     template_name = 'academics/batch_confirm_delete.html'
#     success_url = reverse_lazy('batch-list')

# # # Student Views
# # class StudentListView(ListView):
# #     model = Student
# #     template_name = 'academics/student_list.html'
# #     context_object_name = 'students'

# # class StudentCreateView(CreateView):
# #     model = Student
# #     form_class = StudentForm
# #     template_name = 'academics/student_form.html'
# #     success_url = reverse_lazy('student-list')

# # class StudentUpdateView(UpdateView):
# #     model = Student
# #     form_class = StudentForm
# #     template_name = 'academics/student_form.html'
# #     success_url = reverse_lazy('student-list')

# # class StudentDeleteView(DeleteView):
# #     model = Student
# #     template_name = 'academics/student_confirm_delete.html'
# #     success_url = reverse_lazy('student-list')
