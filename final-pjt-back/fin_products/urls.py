# fin_products/urls.py

from django.urls import path
from .views import fetch_and_save_term_deposits, fetch_and_save_saving_deposits, get_term_deposits, get_saving_deposits, product_based_recommendation


urlpatterns = [
    # DB 저장용
    path('fetch/term_deposits/', fetch_and_save_term_deposits),     
    path('fetch/saving_deposits/', fetch_and_save_saving_deposits), 

    # 프론트 렌더링용
    path('term_deposits/', get_term_deposits),         
    path('saving_deposits/', get_saving_deposits),     
    path('recommend/product-based/', product_based_recommendation),
]
