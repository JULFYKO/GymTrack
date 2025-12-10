from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
import json
from .models import Gym

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class GymView(View):
    def get(self, request, *args, **kwargs):
        gyms = list(Gym.objects.values())
        return JsonResponse(gyms, safe=False)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        gym = Gym.objects.create(**data)
        return JsonResponse({'id': gym.id, 'message': 'Gym created successfully'})

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        gym_id = kwargs.get('id')
        try:
            gym = Gym.objects.get(id=gym_id)
            for key, value in data.items():
                setattr(gym, key, value)
            gym.save()
            return JsonResponse({'message': 'Gym updated successfully'})
        except Gym.DoesNotExist:
            return JsonResponse({'error': 'Gym not found'}, status=404)

    def delete(self, request, *args, **kwargs):
        gym_id = kwargs.get('id')
        try:
            gym = Gym.objects.get(id=gym_id)
            gym.delete()
            return JsonResponse({'message': 'Gym deleted successfully'})
        except Gym.DoesNotExist:
            return JsonResponse({'error': 'Gym not found'}, status=404)
    def list_treners(self, request, *args, **kwargs):
        gym_id = kwargs.get('id')
        try:
            gym = Gym.objects.get(id=gym_id)
            trainers = list(gym.trainers.values())
            return JsonResponse(trainers, safe=False)
        except Gym.DoesNotExist:
            return JsonResponse({'error': 'Gym not found'}, status=404)