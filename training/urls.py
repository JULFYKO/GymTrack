from django.urls import path
from . import views

app_name = 'training'

urlpatterns = [
    path('', views.session_list, name='session_list'),
    path('start/', views.start_session, name='start_session'),
    path('<int:pk>/', views.session_detail, name='session_detail'),
    path('<int:pk>/finish/', views.finish_session, name='finish_session'),
    path('<int:pk>/summary/', views.workout_summary, name='workout_summary'),
    path('analytics/', views.analytics, name='analytics'),
    path('analytics/exercise/<int:exercise_id>/', views.exercise_analytics, name='exercise_analytics'),
    path('profile/', views.profile_view, name='profile'),
]