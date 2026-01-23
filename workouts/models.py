from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.validators import FileExtensionValidator
import os

class Exercise(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    main_image = models.ImageField(upload_to="exercises/thumbnails/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    favorited_by = models.ManyToManyField(get_user_model(), related_name="favorite_exercises", blank=True)
    calories_factor = models.DecimalField(max_digits=5, decimal_places=4, default=0.1000)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("workouts:exercise-detail", kwargs={"pk": self.pk})

class ExerciseMedia(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="media")
    file = models.FileField(
        upload_to="exercises/gallery/",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'mp4', 'mov', 'avi'])]
    )
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    TYPE_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='image')

    class Meta:
        ordering = ["order"]

    def save(self, *args, **kwargs):
        ext = os.path.splitext(self.file.name)[1].lower()
        if ext in ['.mp4', '.mov', '.avi']:
            self.type = 'video'
        else:
            self.type = 'image'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.exercise.name} - {self.caption or self.pk}"