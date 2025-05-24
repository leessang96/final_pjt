"""
URL configuration for protoBack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import gold_price, silver_price, copper_price, oil_price, gas_price

urlpatterns = [
    path('gold-price/', gold_price),
    path('silver-price/', silver_price),
    path('copper-price/', copper_price),
    path('oil-price/', oil_price),
    path('gas-price/', gas_price),
]
