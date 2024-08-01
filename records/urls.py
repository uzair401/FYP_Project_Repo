# records/urls.py
from django.urls import path
from . import views

app_name = 'records'

urlpatterns = [
    path('', views.exam_dashboard, name='Exam_dashboard'),
    path('add_record/', views.add_record, name='add_record'),
    # path('<int:id>/', views.record_detail, name='record_detail'),
]
