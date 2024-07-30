# core/urls.py
from django.urls import path
from . import views
from academics.views import department

app_name = 'core'

urlpatterns = [
    path('', department, name='dashboard'),
    path('logout/', views.Logout, name="Logout"),
    path('users/', views.users, name='users_dashboard'),
    path('user/create/', views.user_create, name='user_create'),
    path('user/update/<int:user_id>/', views.user_update, name='user_update'),
    path('user/delete/<int:user_id>/', views.user_delete, name='user_delete'),
    # path('about/', views.about, name='about'),
    # Add more URLs specific to your 'core' app as needed
]
