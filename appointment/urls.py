from django.urls import path
from . import views

urlpatterns = [
    path('', views.AppointmentView.as_view(), name="appointment"),
     path('admin/appointment/approve/<int:id>/', views.approve_appointment, name='approve_appointment'),
    path('admin/appointment/change_time/<int:id>/', views.change_time_appointment, name='change_time_appointment'),
    
]
