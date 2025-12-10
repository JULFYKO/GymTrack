from django.urls import path
from . import views

app_name = 'workouts'

urlpatterns = [
    path('', views.index, name='index'),
    path('exercise/<int:pk>/', views.detail, name='detail'),
    path('tracker/', views.tracker, name='tracker'),
    path('stats/', views.stats, name='stats'),
]
