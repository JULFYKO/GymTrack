from django import forms
from django.forms import inlineformset_factory
from .models import Exercise, TrainingPlan, TrainingPlanItem, ExerciseMedia

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ["name", "description", "main_image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "block w-full rounded bg-slate-700 border border-slate-600 text-slate-100 px-3 py-2"}),
            "description": forms.Textarea(attrs={"class": "block w-full rounded bg-slate-700 border border-slate-600 text-slate-100 px-3 py-2", "rows": 4}),
            "main_image": forms.ClearableFileInput(attrs={"class": "block w-full text-slate-200 file:bg-indigo-600 file:text-white file:border-0 file:rounded file:px-4 file:py-2 hover:file:bg-indigo-700 cursor-pointer"}),
        }

class ExerciseMediaForm(forms.ModelForm):
    class Meta:
        model = ExerciseMedia
        fields = ["file", "caption", "order"]
        widgets = {
            "file": forms.FileInput(attrs={"class": "block w-full text-xs text-slate-300 file:bg-slate-600 file:text-white file:border-0 file:rounded file:px-2 file:py-1"}),
            "caption": forms.TextInput(attrs={"class": "block w-full rounded bg-slate-700 border border-slate-600 text-slate-100 px-2 py-1 text-sm", "placeholder": "Caption"}),
            "order": forms.NumberInput(attrs={"class": "block rounded bg-slate-700 border border-slate-600 text-slate-100 px-2 py-1 text-sm", "style": "width: 60px"}),
        }

# FormSet пов'язує Exercise з ExerciseMedia
ExerciseMediaFormSet = inlineformset_factory(
    Exercise,
    ExerciseMedia,
    form=ExerciseMediaForm,
    extra=0, # Не створювати пусті поля автоматично (робимо це через JS)
    can_delete=True
)


class TrainingPlanForm(forms.ModelForm):
    class Meta:
        model = TrainingPlan
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "block w-full rounded bg-slate-700 border border-slate-600 text-slate-100 px-3 py-2",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "block w-full rounded bg-slate-700 border border-slate-600 text-slate-100 px-3 py-2",
                    "rows": 3,
                }
            ),
        }


TrainingPlanItemFormSet = inlineformset_factory(
    TrainingPlan,
    TrainingPlanItem,
    fields=("exercise", "order", "default_sets", "default_reps", "note"),
    extra=1,
    widgets={
        "exercise": forms.Select(
            attrs={"class": "block w-full rounded bg-slate-700 border border-slate-600 text-slate-100 px-3 py-2"}
        ),
        "order": forms.NumberInput(
            attrs={"class": "block rounded bg-slate-700 border border-slate-600 text-slate-100 px-2 py-1", "style": "width:100px;"}
        ),
        "default_sets": forms.NumberInput(
            attrs={"class": "block rounded bg-slate-700 border border-slate-600 text-slate-100 px-2 py-1", "style": "width:100px;"}
        ),
        "default_reps": forms.TextInput(
            attrs={"class": "block w-full rounded bg-slate-700 border border-slate-600 text-slate-100 px-3 py-2"}
        ),
        "note": forms.Textarea(
            attrs={"class": "block w-full rounded bg-slate-700 border border-slate-600 text-slate-100 px-3 py-2", "rows": 2}
        ),
    },
    can_delete=True,
)


class ExerciseImageForm(forms.ModelForm):
    class Meta:
        model = ExerciseMedia
        fields = ("file", "caption", "order", "type")
        widgets = {
            "file": forms.ClearableFileInput(attrs={"class": "block w-full text-slate-200"}),
            "caption": forms.TextInput(attrs={"class": "block w-full rounded bg-slate-700 border border-slate-600 text-slate-100 px-3 py-2"}),
            "order": forms.NumberInput(attrs={"class": "block rounded bg-slate-700 border border-slate-600 text-slate-100 px-2 py-1", "style": "width:100px;"}),
            "type": forms.Select(attrs={"class": "block w-full rounded bg-slate-700 border border-slate-600 text-slate-100 px-3 py-2"}),
        }


ExerciseMediaExtraFormSet = inlineformset_factory(
    Exercise,
    ExerciseMedia,
    form=ExerciseMediaForm,
    fields=("file", "caption", "order", "type"),
    extra=1,
    can_delete=True,
)
