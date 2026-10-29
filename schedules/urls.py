from django.urls import path
from .views import doctor_schedule, days_off, slot_create

urlpatterns = [
    path('doctor/<int:doctor_id>/', doctor_schedule, name='doctor_schedule'),
    path('doctor/<int:doctor_id>/days-off/', days_off, name='days_off'),
    path('doctor/<int:doctor_id>/slots/create/', slot_create, name='slot_create'),
]
