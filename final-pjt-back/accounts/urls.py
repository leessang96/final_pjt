from django.urls import path
from . import views

urlpatterns = [
    path('mypage/', views.mypage_view)
]
