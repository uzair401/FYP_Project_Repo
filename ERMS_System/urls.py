from core import views as core_views 
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('core/logout', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('core.urls',namespace='core')),
    path('records/', include('records.urls',namespace='records')),
    path('students/', include('students.urls', namespace='students')),
    path('academics/', include('academics.urls', namespace='academics')),
]

handler400 = 'core.views.error_400_view'
handler403 = 'core.views.error_403_view'
handler404 = 'core.views.error_404_view'
handler500 = 'core.views.error_500_view'