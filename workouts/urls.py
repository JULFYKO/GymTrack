from django.urls import path
from . import views

app_name = "workouts"

urlpatterns = [
    # Exercises
    path("exercises/", views.ExerciseListView.as_view(), name="exercise-list"),
    path("exercises/new/", views.ExerciseCreateView.as_view(), name="exercise-create"),
    path("exercises/<int:pk>/", views.ExerciseDetailView.as_view(), name="exercise-detail"),
    path("exercises/<int:pk>/edit/", views.ExerciseUpdateView.as_view(), name="exercise-edit"),
    path("exercises/<int:pk>/delete/", views.ExerciseDeleteView.as_view(), name="exercise-delete"),

    # Training plans
    path("plans/", views.TrainingPlanListView.as_view(), name="trainingplan-list"),
    path("plans/new/", views.TrainingPlanCreateView.as_view(), name="trainingplan-create"),
    path("plans/<int:pk>/", views.TrainingPlanDetailView.as_view(), name="trainingplan-detail"),
    path("plans/<int:pk>/edit/", views.TrainingPlanUpdateView.as_view(), name="trainingplan-edit"),
    path("plans/<int:pk>/delete/", views.TrainingPlanDeleteView.as_view(), name="trainingplan-delete"),
]
