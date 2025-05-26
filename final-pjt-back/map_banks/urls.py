# map_banks/urls.py
from django.urls import path
from .views import search_nearby_banks

urlpatterns = [
    path('nearby-banks/', search_nearby_banks),
]