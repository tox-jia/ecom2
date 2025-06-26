from django.urls import path
from . import views

urlpatterns = [
    path('', views.time_checkout, name='time_checkout'),
    path('time_records/', views.time_records, name='time_records'),
    path('time_report/', views.time_report, name='time_report'),
    path('time_settings/', views.time_settings, name='time_settings'),
    path('ajax/records_toggle/', views.ajax_records_toggle, name='ajax_records_toggle'),
]