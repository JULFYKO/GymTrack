from django import forms
from .models import ExerciseEntry, UserProfile
from workouts.models import Exercise as WorkoutExercise

class ExerciseEntryForm(forms.ModelForm):
    exercise = forms.ModelChoiceField(queryset=WorkoutExercise.objects.all(), required=True, widget=forms.Select(attrs={'class': 'w-full bg-slate-800 text-slate-100 px-2 py-1 rounded'}))

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

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['weight', 'height', 'age', 'gender', 'activity_level', 'goal']
        labels = {
            'weight': 'Вага (кг)',
            'height': 'Зріст (см)',
            'age': 'Вік',
            'gender': 'Стать',
            'activity_level': 'Рівень активності',
            'goal': 'Ваша ціль',
        }
        widgets = {
            'weight': forms.NumberInput(attrs={'class': 'w-full bg-slate-800 text-white rounded p-2 border border-slate-700'}),
            'height': forms.NumberInput(attrs={'class': 'w-full bg-slate-800 text-white rounded p-2 border border-slate-700'}),
            'age': forms.NumberInput(attrs={'class': 'w-full bg-slate-800 text-white rounded p-2 border border-slate-700'}),
            'gender': forms.Select(attrs={'class': 'w-full bg-slate-800 text-white rounded p-2 border border-slate-700'}),
            'activity_level': forms.Select(attrs={'class': 'w-full bg-slate-800 text-white rounded p-2 border border-slate-700'}),
            'goal': forms.Select(attrs={'class': 'w-full bg-slate-800 text-white rounded p-2 border border-slate-700'}),
        }