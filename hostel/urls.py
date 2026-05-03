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
    path('assign-room/<int:guest_id>/', views.assign_room, name='assign_room'),


    path('r_order/', views.r_order, name='r_order'),

    path('monthly_job/', views.monthly_job, name='monthly_job'),
    path('save_payment/', views.save_payment, name='save_payment'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('mark_done/', views.mark_done, name='mark_done'),

    path('hr/', views.hr, name='hr'),
    path('hr/update/', views.update_hr, name='update_hr'),
]