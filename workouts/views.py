from django.shortcuts import render, get_object_or_404, redirect
from .models import Exercise, ExerciseLog
from django.utils import timezone


def index(request):
    exercises = Exercise.objects.all().order_by('name')
    return render(request, 'workouts/index.html', {'exercises': exercises})


def detail(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    logs = exercise.logs.all()[:20]
    return render(request, 'workouts/detail.html', {'exercise': exercise, 'logs': logs})


def tracker(request):
    # simple tracker page — POST handling is minimal for initial scaffold
    if request.method == 'POST':
        exercise_id = request.POST.get('exercise')
        date = request.POST.get('date') or timezone.now().date()
        weight = request.POST.get('weight') or None
        reps = request.POST.get('reps') or None
        sets = request.POST.get('sets') or 1
        notes = request.POST.get('notes') or ''
        if exercise_id:
            try:
                ex = Exercise.objects.get(pk=exercise_id)
                ExerciseLog.objects.create(
                    exercise=ex,
                    date=date,
                    weight=weight or None,
                    reps=reps or None,
                    sets=sets or 1,
                    notes=notes,
                )
                return redirect('workouts:tracker')
            except Exercise.DoesNotExist:
                pass

    exercises = Exercise.objects.all().order_by('name')
    recent = ExerciseLog.objects.select_related('exercise')[:20]
    return render(request, 'workouts/tracker.html', {'exercises': exercises, 'recent': recent})


def stats(request):
    # placeholder for stats page — will later aggregate logs
    return render(request, 'workouts/stats.html')
