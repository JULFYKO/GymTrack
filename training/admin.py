from django.contrib import admin
from .models import TrainingSession, ExerciseEntry, Exercise, Medal, Award
from .models import Set

@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'started_at', 'ended_at')


@admin.register(ExerciseEntry)
class ExerciseEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'training', 'name', 'weight', 'reps', 'added_at')


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Medal)
class MedalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'threshold_total_weight')


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('user', 'medal', 'awarded_at')


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ('id', 'entry', 'order', 'weight', 'reps')
from django.contrib import admin

