# records/urls.py
from django.urls import path
from . import views

app_name = 'records'

urlpatterns = [
    path('', views.record_list, name='record_list'),
    # path('<int:id>/', views.record_detail, name='record_detail'),
]
