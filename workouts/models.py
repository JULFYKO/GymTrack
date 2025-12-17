from django.db import models
from django.contrib.auth import get_user_model


# Simple exercise model
class Exercise(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
		return self.name


class TrainingPlan(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	exercises = models.ManyToManyField(
		Exercise, through="TrainingPlanItem", related_name="training_plans", blank=True
	)
	author = models.ForeignKey(
		get_user_model(), null=True, blank=True, on_delete=models.SET_NULL
	)
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

	def __str__(self):
		return f"{self.plan.title} - {self.order}: {self.exercise.name}"
