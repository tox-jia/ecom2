from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkin, name='checkin'),
    path('terms/<int:step>/', views.terms, name='terms'),
    path('summary/', views.summary, name='summary'),
    path('<int:pk>/', views.viewGuest, name='view_guest'),
]