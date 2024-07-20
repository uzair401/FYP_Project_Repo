# academics/urls.py
from django.urls import path
# from .views import (
#     ProgramListView, ProgramCreateView, ProgramUpdateView, ProgramDeleteView,
#     SemesterListView, SemesterCreateView, SemesterUpdateView, SemesterDeleteView,
#     CourseListView, CourseCreateView, CourseUpdateView, CourseDeleteView,
#     BatchListView, BatchCreateView, BatchUpdateView, BatchDeleteView,
#     # StudentListView, StudentCreateView, StudentUpdateView, StudentDeleteView
# )

from . import views
app_name = 'academics'
urlpatterns = [
    path('<int:department_id>/', views.program, name="program"),
    path('batch/<int:program_id>/', views.batch, name="batch"),
    path('semester/<int:program_id>/', views.semester, name="semester"),
    path('course/<int:semester_id>/', views.course, name="course"),

    # path('', ProgramListView.as_view(), name='program-list'),
    # path('programs/create/', ProgramCreateView.as_view(), name='program-create'),
    # path('programs/<int:pk>/update/', ProgramUpdateView.as_view(), name='program-update'),
    # path('programs/<int:pk>/delete/', ProgramDeleteView.as_view(), name='program-delete'),

    # path('semesters/', SemesterListView.as_view(), name='semester-list'),
    # path('semesters/create/', SemesterCreateView.as_view(), name='semester-create'),
    # path('semesters/<int:pk>/update/', SemesterUpdateView.as_view(), name='semester-update'),
    # path('semesters/<int:pk>/delete/', SemesterDeleteView.as_view(), name='semester-delete'),

    # path('courses/', CourseListView.as_view(), name='course-list'),
    # path('courses/create/', CourseCreateView.as_view(), name='course-create'),
    # path('courses/<int:pk>/update/', CourseUpdateView.as_view(), name='course-update'),
    # path('courses/<int:pk>/delete/', CourseDeleteView.as_view(), name='course-delete'),

    # path('batches/', BatchListView.as_view(), name='batch-list'),
    # path('batches/create/', BatchCreateView.as_view(), name='batch-create'),
    # path('batches/<int:pk>/update/', BatchUpdateView.as_view(), name='batch-update'),
    # path('batches/<int:pk>/delete/', BatchDeleteView.as_view(), name='batch-delete'),

#     path('students/', StudentListView.as_view(), name='student-list'),
#     path('students/create/', StudentCreateView.as_view(), name='student-create'),
#     path('students/<int:pk>/update/', StudentUpdateView.as_view(), name='student-update'),
#     path('students/<int:pk>/delete/', StudentDeleteView.as_view(), name='student-delete'),
]
