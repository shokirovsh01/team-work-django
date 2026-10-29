from django.urls import path
from .views import (
    MyAppointmentsView,
    AppointmentBookView,
    AppointmentDetailView,
    AppointmentCancelView,
    AppointmentUpdateView
)

app_name = 'appointments'

urlpatterns = [
    path('my/', MyAppointmentsView.as_view(), name='my_appointments'),
    path('book/<int:doctor_id>/', AppointmentBookView.as_view(), name='appointment_book'),
    path('<int:pk>/', AppointmentDetailView.as_view(), name='appointment_detail'),
    path('<int:pk>/cancel/', AppointmentCancelView.as_view(), name='appointment_cancel'),
    path('<int:pk>/edit/', AppointmentUpdateView.as_view(), name='appointment_update'),
]