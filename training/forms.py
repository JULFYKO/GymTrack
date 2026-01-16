from django import forms
from .models import ExerciseEntry
from workouts.models import Exercise as WorkoutExercise


class ExerciseEntryForm(forms.ModelForm):
    # Only allow selection from existing exercises; saved as `name` on the entry
    exercise = forms.ModelChoiceField(queryset=WorkoutExercise.objects.all(), required=True,
                                      widget=forms.Select(attrs={'class': 'w-full bg-slate-800 text-slate-100 px-2 py-1 rounded'}))

    class Meta:
        model = ExerciseEntry
        fields = ['exercise', 'weight', 'reps']
        widgets = {
            'weight': forms.NumberInput(attrs={'class': 'border rounded px-2 py-1 w-32 bg-slate-800 text-slate-100', 'step': '0.5'}),
            'reps': forms.NumberInput(attrs={'class': 'border rounded px-2 py-1 w-20 bg-slate-800 text-slate-100', 'min': 0}),
        }

    def save(self, commit=True):
        inst = super().save(commit=False)
        ex = self.cleaned_data.get('exercise')
        if ex:
            inst.name = ex.name
        if commit:
            inst.save()
        return inst
