from django.urls import path
from .views import *

app_name = 'appointments'

urlpatterns = [
    path('my/', MyAppointmentsView.as_view(), name='my_appointments'),
    path('book/<int:doctor_id>/', AppointmentBookView.as_view(), name='appointment_book'),
    path('<int:pk>/', AppointmentDetailView.as_view(), name='appointment_detail'),
    path('<int:pk>/cancel/', AppointmentCancelView.as_view(), name='appointment_cancel'),
    path('<int:pk>/edit/', AppointmentUpdateView.as_view(), name='appointment_update'),
    path('available/<int:doctor_id>/', AppointmentsAvailableView.as_view(), name='appointment_available'),
    path('doctor/', DoctorAppointmentsView.as_view(), name='doctor_appointments'),
    path('<int:pk>/confirm/', AppointmentConfirmView.as_view(), name='appointment_confirm'),
    path('<int:pk>/complete/', AppointmentCompleteView.as_view(), name='appointment_complete'),
    
]