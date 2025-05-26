from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list),
    path('articles/<int:article_pk>/', views.article_detail),
    path('articles/<int:article_pk>/comments/', views.comment_list_create),
    path('articles/comments/<int:comment_pk>/', views.comment_update_delete),

]
