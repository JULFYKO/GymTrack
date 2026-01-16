from django.db import models
from django.conf import settings
from decimal import Decimal


class TrainingSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Training #{self.id} - {self.user or 'anonymous'} - {self.started_at.date()}"

    @property
    def total_weight(self):
        total = Decimal('0')
        for e in self.exercises.all():
            total += e.total_weight
        return total


class Exercise(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ExerciseEntry(models.Model):
    training = models.ForeignKey(TrainingSession, related_name='exercises', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    weight = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    reps = models.PositiveIntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.weight}kg x{self.reps}"

    @property
    def total_weight(self):
        # If there are sets, sum them; otherwise fall back to single weight/reps
        sets = getattr(self, 'sets', None)
        if sets and sets.exists():
            total = Decimal('0')
            for s in sets.all():
                total += Decimal(s.weight) * Decimal(s.reps)
            return total
        return Decimal(self.weight) * Decimal(self.reps)


class Set(models.Model):
    entry = models.ForeignKey(ExerciseEntry, related_name='sets', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=1)
    weight = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    reps = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Set {self.order} - {self.weight}kg x{self.reps}"


class Medal(models.Model):
    """Simple medal scaffold. Add more fields/conditions as needed."""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    threshold_total_weight = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class Award(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    medal = models.ForeignKey(Medal, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)
    training = models.ForeignKey(TrainingSession, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('user', 'medal')

    def __str__(self):
        return f"{self.user} - {self.medal}"
