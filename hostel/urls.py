from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkin, name='checkin'),
    path('<int:pk>/', views.viewGuest, name='view_guest'),

]