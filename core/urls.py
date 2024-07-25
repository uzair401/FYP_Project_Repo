# core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('logout/', views.Logout, name="Logout")
    # path('about/', views.about, name='about'),
    # Add more URLs specific to your 'core' app as needed
]
