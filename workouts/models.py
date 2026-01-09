from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.validators import FileExtensionValidator
import os

class Exercise(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # Це прев'ю (тільки картинка)
    main_image = models.ImageField(upload_to="exercises/thumbnails/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Users who favorited this exercise
    favorited_by = models.ManyToManyField(get_user_model(), related_name="favorite_exercises", blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("workouts:exercise-detail", kwargs={"pk": self.pk})


class ExerciseMedia(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="media")
    # FileField дозволяє і фото, і відео
    file = models.FileField(
        upload_to="exercises/gallery/",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'mp4', 'mov', 'avi'])]
    )
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    # Тип файлу визначатимемо автоматично
    TYPE_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='image')

    class Meta:
        ordering = ["order"]

    def save(self, *args, **kwargs):
        # Автоматичне визначення типу файлу перед збереженням
        ext = os.path.splitext(self.file.name)[1].lower()
        if ext in ['.mp4', '.mov', '.avi']:
            self.type = 'video'
        else:
            self.type = 'image'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.exercise.name} - {self.caption or self.pk}"

# TrainingPlan залишаємо без змін (скорочено для економії місця)
class TrainingPlan(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    exercises = models.ManyToManyField(Exercise, through="TrainingPlanItem", related_name="training_plans", blank=True)
    author = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

class TrainingPlanItem(models.Model):
    plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, related_name="items")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    default_sets = models.PositiveIntegerField(default=3)
    default_reps = models.CharField(max_length=50, blank=True)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ["order"]
        unique_together = (("plan", "exercise", "order"),)