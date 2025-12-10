from django.urls import path
from . import html_views

app_name = 'services'

urlpatterns = [
	path('trainers/', html_views.trainers_list, name='trainers_list'),
]
