from django.db import models
from django.conf import settings
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
    
    ACTIVITY_CHOICES = (
        (Decimal('1.2'), 'Сидячий (без тренувань)'),
        (Decimal('1.375'), 'Легкий (1-3 тренування/тиждень)'),
        (Decimal('1.55'), 'Помірний (3-5 тренувань/тиждень)'),
        (Decimal('1.725'), 'Активний (6-7 тренувань/тиждень)'),
        (Decimal('1.9'), 'Дуже активний (фізична робота + спорт)'),
    )

    GOAL_CHOICES = (
        ('LOSE', 'Схуднення (-500 ккал)'),
        ('MAINTAIN', 'Підтримання ваги'),
        ('GAIN', 'Набір маси (+500 ккал)'),
    )
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=70.0)
    height = models.DecimalField(max_digits=5, decimal_places=2, default=170.0)
    age = models.PositiveIntegerField(default=25)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    activity_level = models.DecimalField(max_digits=4, decimal_places=3, choices=ACTIVITY_CHOICES, default=Decimal('1.2'))
    goal = models.CharField(max_length=10, choices=GOAL_CHOICES, default='MAINTAIN')
    target_calories = models.PositiveIntegerField(default=2000)

    def __str__(self):
        return f"Profile of {self.user.username}"

    @property
    def bmi(self):
        h_m = float(self.height) / 100
        w_kg = float(self.weight)
        if h_m > 0:
            return round(w_kg / (h_m ** 2), 1)
        return 0.0

    @property
    def bmr(self):
        w = float(self.weight)
        h = float(self.height)
        a = self.age
        base = (10 * w) + (6.25 * h) - (5 * a)
        if self.gender == 'M':
            return round(base + 5)
        return round(base - 161)

    def calculate_target_calories(self):
        bmr_val = self.bmr
        tdee = bmr_val * float(self.activity_level)
        if self.goal == 'LOSE':
            return round(tdee - 500)
        elif self.goal == 'GAIN':
            return round(tdee + 500)
        else:
            return round(tdee)

    def save(self, *args, **kwargs):
        self.target_calories = self.calculate_target_calories()
        super().save(*args, **kwargs)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

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

    @property
    def total_calories_burned(self):
        total = Decimal('0')
        for e in self.exercises.all():
            total += Decimal(str(e.calories_burned))
        return total

    def is_finished(self):
        return self.ended_at is not None

class Exercise(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class ExerciseEntry(models.Model):
    training = models.ForeignKey(TrainingSession, related_name='exercises', on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200) 
    calories_factor = models.DecimalField(max_digits=5, decimal_places=4, default=0.1)
    weight = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    reps = models.PositiveIntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.sets_count} sets"

    def save(self, *args, **kwargs):
        if not self.name and self.exercise:
            self.name = self.exercise.name
        super().save(*args, **kwargs)

    @property
    def total_weight(self):
        if self.sets.exists():
            total = Decimal('0')
            for s in self.sets.all():
                total += s.weight * s.reps
            return total
        return self.weight * self.reps

    @property
    def sets_count(self):
        return self.sets.count()
    
    @property
    def calories_burned(self):
        user_weight = 70.0
        if self.training.user and hasattr(self.training.user, 'profile'):
             user_weight = float(self.training.user.profile.weight)
        factor = float(self.calories_factor)
        return round(factor * user_weight * self.sets_count, 1)

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