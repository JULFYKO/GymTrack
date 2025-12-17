from django import forms
from django.forms import inlineformset_factory
from .models import Exercise, TrainingPlan, TrainingPlanItem


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if len(name) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long.")

        qs = Exercise.objects.filter(name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("An exercise with this name already exists.")

        return name


class TrainingPlanForm(forms.ModelForm):
    class Meta:
        model = TrainingPlan
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


TrainingPlanItemFormSet = inlineformset_factory(
    TrainingPlan,
    TrainingPlanItem,
    fields=("exercise", "order", "default_sets", "default_reps", "note"),
    extra=1,
    widgets={
        "exercise": forms.Select(attrs={"class": "form-select"}),
        "order": forms.NumberInput(attrs={"class": "form-control", "style": "width:100px;"}),
        "default_sets": forms.NumberInput(attrs={"class": "form-control", "style": "width:100px;"}),
        "default_reps": forms.TextInput(attrs={"class": "form-control"}),
        "note": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
    },
    can_delete=True,
)
