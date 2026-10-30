from django import forms
from .models import Appointment

class AppointmentBookForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [ 'appointment_date']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }