from django.urls import path
from . import views

urlpatterns = [
    path('mypage/', views.mypage_view),
    path('add-product/', views.add_sub_product),  # 내 상품 라우트
]
