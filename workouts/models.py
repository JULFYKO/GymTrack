from django.db import models


class Exercise(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ExerciseLog(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField()
    weight = models.FloatField(blank=True, null=True, help_text='Weight used (kg or lb)')
    reps = models.PositiveIntegerField(blank=True, null=True)
    sets = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.exercise.name} — {self.date} ({self.sets}×{self.reps or '-'} @ {self.weight or '-'})"
