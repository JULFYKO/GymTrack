from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from .models import Exercise, TrainingPlan
from .forms import ExerciseForm, TrainingPlanForm, TrainingPlanItemFormSet, ExerciseMediaFormSet




class ExerciseListView(generic.ListView):
	model = Exercise
	template_name = "workouts/exercise_list.html"
	context_object_name = "exercises"

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		user = self.request.user
		if user.is_authenticated:
			ctx["favorite_exercises"] = user.favorite_exercises.all()
			ctx["favorites_count"] = ctx["favorite_exercises"].count()
		else:
			ctx["favorite_exercises"] = []
			ctx["favorites_count"] = 0
		return ctx


class ExerciseDetailView(generic.DetailView):
	model = Exercise
	template_name = "workouts/exercise_detail.html"
	context_object_name = "exercise"

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		user = self.request.user
		exercise = self.get_object()
		ctx["is_favorite"] = False
		if user.is_authenticated:
			ctx["is_favorite"] = exercise.favorited_by.filter(pk=user.pk).exists()
		return ctx


class ExerciseDeleteView(generic.DeleteView):
	model = Exercise
	template_name = "workouts/exercise_confirm_delete.html"
	success_url = reverse_lazy("workouts:exercise-list")


class ExerciseCreateView(generic.CreateView):
    model = Exercise
    form_class = ExerciseForm
    template_name = "workouts/exercise_form.html"
    success_url = reverse_lazy("workouts:exercise-list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            # Якщо це POST запит, заповнюємо формсет даними
            ctx['media_formset'] = ExerciseMediaFormSet(self.request.POST, self.request.FILES)
        else:
            # Якщо це GET запит, створюємо порожній формсет
            ctx['media_formset'] = ExerciseMediaFormSet()
        return ctx

    def form_valid(self, form):
        context = self.get_context_data()
        media_formset = context['media_formset']
        
        if media_formset.is_valid():
            self.object = form.save() # Спочатку зберігаємо саму вправу
            media_formset.instance = self.object # Прив'язуємо галерею до цієї вправи
            media_formset.save() # Зберігаємо галерею
            return super().form_valid(form)
        else:
            # Якщо помилка у формсеті, повертаємо сторінку з помилками
            return self.render_to_response(self.get_context_data(form=form))


class ExerciseUpdateView(generic.UpdateView):
    model = Exercise
    form_class = ExerciseForm
    template_name = "workouts/exercise_form.html"
    success_url = reverse_lazy("workouts:exercise-list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx['media_formset'] = ExerciseMediaFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            ctx['media_formset'] = ExerciseMediaFormSet(instance=self.object)
        return ctx

    def form_valid(self, form):
        context = self.get_context_data()
        media_formset = context['media_formset']
        
        if media_formset.is_valid():
            self.object = form.save()
            media_formset.instance = self.object
            media_formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


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


class RegisterView(generic.CreateView):
	form_class = UserCreationForm
	template_name = 'registration/register.html'
	success_url = reverse_lazy('workouts:exercise-list')

	def form_valid(self, form):
		response = super().form_valid(form)
		user = self.object
		login(self.request, user)
		return response


def logout_view(request):
	"""Logout view that accepts GET and POST and redirects to home."""
	auth_logout(request)
	return redirect('home')


@login_required
def toggle_favorite(request, pk):
	exercise = get_object_or_404(Exercise, pk=pk)
	user = request.user
	if user in exercise.favorited_by.all():
		exercise.favorited_by.remove(user)
	else:
		exercise.favorited_by.add(user)

	next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or reverse_lazy("workouts:exercise-list")
	return redirect(next_url)

	def post(self, request, pk):
		return trainingplan_form_view(request, pk=pk)
