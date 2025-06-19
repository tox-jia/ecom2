from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('new/', views.create_post, name='create_post'),
    path('<int:pk>/', views.view_post, name='view_post'),
]