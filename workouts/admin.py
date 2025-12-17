from django.contrib import admin
from .models import Exercise, TrainingPlan, TrainingPlanItem


class TrainingPlanItemInline(admin.TabularInline):
	model = TrainingPlanItem
	extra = 1


@admin.register(TrainingPlan)
class TrainingPlanAdmin(admin.ModelAdmin):
	list_display = ("title", "author", "created_at")
	inlines = (TrainingPlanItemInline,)


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
	list_display = ("name", "created_at")


@admin.register(TrainingPlanItem)
class TrainingPlanItemAdmin(admin.ModelAdmin):
	list_display = ("plan", "exercise", "order", "default_sets")
