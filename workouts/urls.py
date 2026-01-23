from django.urls import path
from . import views

app_name = "workouts"

urlpatterns = [
    path("exercises/", views.ExerciseListView.as_view(), name="exercise-list"),
    path("exercises/new/", views.ExerciseCreateView.as_view(), name="exercise-create"),
    path("exercises/<int:pk>/", views.ExerciseDetailView.as_view(), name="exercise-detail"),
    path("exercises/<int:pk>/edit/", views.ExerciseUpdateView.as_view(), name="exercise-edit"),
    path("exercises/<int:pk>/delete/", views.ExerciseDeleteView.as_view(), name="exercise-delete"),
    path("exercises/<int:pk>/favorite/", views.toggle_favorite, name="exercise-favorite"),

]