"""
URL configuration for Django project.
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from workouts.views import RegisterView, logout_view

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('workouts/', include('workouts.urls')),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)