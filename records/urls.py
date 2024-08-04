from django.urls import path
from . import views

app_name = 'records'

urlpatterns = [
    path('', views.exam_dashboard, name='Exam_dashboard'),
    path('add_record/', views.add_record, name='add_record'),
    path('batches/<int:exam_record_id>/', views.batches, name='batches'),
    path('update_batch/<int:id>/', views.update_batch, name="update_batch"),
    # path('<int:id>/', views.record_detail, name='record_detail'),
]
