from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from urllib.parse import quote
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, F, Max

from .models import TrainingSession, ExerciseEntry, Medal, Award, Set
from workouts.models import Exercise as WorkoutExercise
from .forms import ExerciseEntryForm


def session_list(request):
    sessions = TrainingSession.objects.order_by('-started_at')[:50]
    return render(request, 'training/session_list.html', {'sessions': sessions})


def start_session(request):
    session = TrainingSession.objects.create(user=request.user if request.user.is_authenticated else None,
                                             started_at=timezone.now())
    return redirect('training:session_detail', pk=session.pk)


def session_detail(request, pk):
    session = get_object_or_404(TrainingSession, pk=pk)
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST.get('action')
            if action == 'add_exercise':
                # enforce selection flow: redirect user to exercises list to pick an exercise
                next_url = request.path
                return redirect(f"/workouts/exercises/?session={session.pk}&next={quote(next_url)}")
            elif action == 'add_exercise_from_library':
                exercise_id = request.POST.get('exercise_id')
                try:
                    ex = WorkoutExercise.objects.get(pk=exercise_id)
                    entry = ExerciseEntry.objects.create(training=session, name=ex.name)
                    Set.objects.create(entry=entry, order=1, weight=0, reps=0)
                except WorkoutExercise.DoesNotExist:
                    pass
                return redirect('training:session_detail', pk=pk)
            elif action == 'add_set':
                entry_id = request.POST.get('entry_id')
                entry = get_object_or_404(ExerciseEntry, pk=entry_id, training=session)
                last_order = entry.sets.aggregate(max_order=Max('order'))['max_order'] or 0
                Set.objects.create(entry=entry, order=last_order + 1, weight=0, reps=0)
                return redirect('training:session_detail', pk=pk)
            elif action == 'delete_set':
                set_id = request.POST.get('set_id')
                s = get_object_or_404(Set, pk=set_id, entry__training=session)
                entry = s.entry
                s.delete()
                # re-order remaining sets
                for i, s2 in enumerate(entry.sets.order_by('order'), start=1):
                    if s2.order != i:
                        s2.order = i
                        s2.save()
                return redirect('training:session_detail', pk=pk)
            elif action == 'delete_entry':
                entry_id = request.POST.get('entry_id')
                entry = get_object_or_404(ExerciseEntry, pk=entry_id, training=session)
                entry.delete()
                return redirect('training:session_detail', pk=pk)
            elif action == 'update_set':
                set_id = request.POST.get('set_id')
                weight = request.POST.get('weight') or 0
                reps = request.POST.get('reps') or 0
                s = get_object_or_404(Set, pk=set_id, entry__training=session)
                s.weight = weight
                s.reps = reps
                s.save()
                return redirect('training:session_detail', pk=pk)
            elif action in ('inc', 'dec'):
                entry_id = request.POST.get('entry_id')
                entry = get_object_or_404(ExerciseEntry, pk=entry_id, training=session)
                if action == 'inc':
                    entry.reps += 1
                else:
                    if entry.reps > 0:
                        entry.reps -= 1
                entry.save()
                return redirect('training:session_detail', pk=pk)
    else:
        form = ExerciseEntryForm()

    exercises = session.exercises.order_by('added_at').prefetch_related('sets')
    total = session.total_weight

    # prepare per-entry aggregates for template (total reps, total weight)
    exercise_infos = []
    for e in exercises:
        total_reps = sum([s.reps for s in e.sets.all()])
        exercise_infos.append({'entry': e, 'total_reps': total_reps, 'total_weight': e.total_weight})

    # available exercises (library)
    try:
        available_exercises = WorkoutExercise.objects.all()
    except Exception:
        available_exercises = []
    return render(request, 'training/session_detail.html', {
        'session': session,
        'form': form,
        'exercises': exercises,
        'exercise_infos': exercise_infos,
        'total': total,
        'available_exercises': available_exercises,
    })


def finish_session(request, pk):
    session = get_object_or_404(TrainingSession, pk=pk)
    session.ended_at = timezone.now()
    session.save()

    # Award medals if thresholds met
    if session.user and session.user.is_authenticated:
        total_all = TrainingSession.objects.filter(user=session.user).aggregate(total=Sum(F('exercises__weight') * F('exercises__reps')))['total'] or 0
        medals = Medal.objects.all()
        for m in medals:
            try:
                Award.objects.get(user=session.user, medal=m)
            except Award.DoesNotExist:
                if total_all >= m.threshold_total_weight:
                    Award.objects.create(user=session.user, medal=m, training=session)

    return redirect('training:session_detail', pk=pk)


def workout_summary(request, pk):
    session = get_object_or_404(TrainingSession, pk=pk)
    # only show summary for finished sessions
    if not session.ended_at:
        return redirect('training:session_detail', pk=pk)
    exercises = session.exercises.prefetch_related('sets')
    total = session.total_weight
    duration = None
    if session.ended_at and session.started_at:
        duration = session.ended_at - session.started_at
    return render(request, 'training/workout_summary.html', {
        'session': session,
        'exercises': exercises,
        'total': total,
        'duration': duration,
    })


def analytics(request):
    # Simple analytics: total weight all time, by day, per session history
    qs = TrainingSession.objects.all()
    total_all = 0
    sessions = []
    for s in qs.order_by('-started_at'):
        sessions.append({'session': s, 'total': s.total_weight})
        total_all += s.total_weight

    # by day
    by_day = {}
    for s in qs:
        day = s.started_at.date()
        by_day.setdefault(day, 0)
        by_day[day] += float(s.total_weight)

    medals = []
    if request.user.is_authenticated:
        medals = Award.objects.filter(user=request.user).select_related('medal')

    return render(request, 'training/analytics.html', {
        'total_all': total_all,
        'sessions': sessions,
        'by_day': sorted(by_day.items()),
        'medals': medals,
    })


def exercise_analytics(request, exercise_id):
    """Per-exercise analytics: per-session reps and total weight, personal totals and medal tiers."""
    ex = get_object_or_404(WorkoutExercise, pk=exercise_id)

    # Aggregate ExerciseEntry by training session for this exercise name
    entries = ExerciseEntry.objects.filter(name=ex.name).select_related('training').prefetch_related('sets')
    per_session = {}
    for e in entries:
        tid = e.training.pk
        reps = sum([s.reps for s in e.sets.all()]) if e.sets.exists() else e.reps
        weight = float(e.total_weight)
        if tid not in per_session:
            per_session[tid] = {'session': e.training, 'reps': 0, 'weight': 0.0}
        per_session[tid]['reps'] += reps
        per_session[tid]['weight'] += weight

    # Order by session date
    sessions = sorted(per_session.values(), key=lambda x: x['session'].started_at)

    labels = [s['session'].started_at.strftime('%Y-%m-%d') for s in sessions]
    weights = [s['weight'] for s in sessions]
    reps = [s['reps'] for s in sessions]

    # User-specific totals
    user_total_weight = 0.0
    user_total_reps = 0
    if request.user.is_authenticated:
        for s in sessions:
            if s['session'].user_id == request.user.id:
                user_total_weight += s['weight']
                user_total_reps += s['reps']

    # Determine global maxima to compute relative medal tiers
    global_max_weight = max(weights) if weights else 0.0
    global_max_reps = max(reps) if reps else 0

    def tier(value, maximum):
        if maximum <= 0:
            return None
        p = value / maximum
        if p >= 0.9:
            return 'gold'
        if p >= 0.6:
            return 'silver'
        if p >= 0.3:
            return 'bronze'
        return None

    weight_tier = tier(user_total_weight, global_max_weight)
    reps_tier = tier(user_total_reps, global_max_reps)

    return render(request, 'training/exercise_analytics.html', {
        'exercise': ex,
        'labels': labels,
        'weights': weights,
        'reps': reps,
        'user_total_weight': user_total_weight,
        'user_total_reps': user_total_reps,
        'weight_tier': weight_tier,
        'reps_tier': reps_tier,
    })

