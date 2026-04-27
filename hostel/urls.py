from django.urls import path
from . import views

urlpatterns = [
    path('', views.language, name='language'),
    path('checkin/', views.checkin, name='checkin'),

    path('terms/<int:step>/', views.terms, name='terms'),
    path('summary/', views.summary, name='summary'),
    path('glist/', views.gList, name='glist'),
    path('update-room/', views.update_room, name='update_room'),
    path('clean/', views.clean, name='clean'),
    path('reset-rooms/', views.reset_rooms, name='reset_rooms'),


    path('access/', views.access_gate, name='access'),
    path('clean/', views.clean, name='clean'),
    path('assign-room/<int:guest_id>/', views.assign_room, name='assign_room'),
]