from django.shortcuts import render
from .models import GymTrainer

def trainers_list(request):
    """Render a Bootstrap-based list of gym trainers."""
    trainers = GymTrainer.objects.all().order_by('last_name')
    return render(request, 'services/list.html', {'trainers': trainers})
