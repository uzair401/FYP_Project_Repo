# academics/urls.py
from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    path('', views.academic_list, name='academic_list'),
    # path('<int:id>/', views.academic_detail, name='academic_detail'),
]
