from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views import generic
from .models import Exercise, TrainingPlan
from .forms import ExerciseForm, TrainingPlanForm, TrainingPlanItemFormSet




class ExerciseListView(generic.ListView):
	model = Exercise
	template_name = "workouts/exercise_list.html"
	context_object_name = "exercises"


class ExerciseDetailView(generic.DetailView):
	model = Exercise
	template_name = "workouts/exercise_detail.html"
	context_object_name = "exercise"


class ExerciseDeleteView(generic.DeleteView):
	model = Exercise
	template_name = "workouts/exercise_confirm_delete.html"
	success_url = reverse_lazy("workouts:exercise-list")


class ExerciseCreateView(generic.CreateView):
	model = Exercise
	form_class = ExerciseForm
	template_name = "workouts/exercise_form.html"
	success_url = reverse_lazy("workouts:exercise-list")


class ExerciseUpdateView(generic.UpdateView):
	model = Exercise
	form_class = ExerciseForm
	template_name = "workouts/exercise_form.html"
	success_url = reverse_lazy("workouts:exercise-list")


class TrainingPlanListView(generic.ListView):
	model = TrainingPlan
	template_name = "workouts/trainingplan_list.html"
	context_object_name = "plans"


class TrainingPlanDetailView(generic.DetailView):
	model = TrainingPlan
	template_name = "workouts/trainingplan_detail.html"
	context_object_name = "plan"


class TrainingPlanDeleteView(generic.DeleteView):
	model = TrainingPlan
	template_name = "workouts/trainingplan_confirm_delete.html"
	success_url = reverse_lazy("workouts:trainingplan-list")


def trainingplan_form_view(request, pk=None):
	if pk:
		plan = TrainingPlan.objects.get(pk=pk)
	else:
		plan = None

	if request.method == "POST":
		form = TrainingPlanForm(request.POST, instance=plan)
		formset = TrainingPlanItemFormSet(request.POST, instance=form.instance)
		if form.is_valid() and formset.is_valid():
			plan = form.save()
			formset.instance = plan
			formset.save()
			return redirect("workouts:trainingplan-list")
	else:
		form = TrainingPlanForm(instance=plan)
		formset = TrainingPlanItemFormSet(instance=plan)

	return render(
		request,
		"workouts/trainingplan_form.html",
		{"form": form, "formset": formset, "plan": plan},
	)


class TrainingPlanCreateView(generic.View):
	def get(self, request):
		return trainingplan_form_view(request)

	def post(self, request):
		return trainingplan_form_view(request)


class TrainingPlanUpdateView(generic.View):
	def get(self, request, pk):
		return trainingplan_form_view(request, pk=pk)

	def post(self, request, pk):
		return trainingplan_form_view(request, pk=pk)
