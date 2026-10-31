from django import forms
from .models import Clinic, ClinicAnnouncement

class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = ['name', 'description', 'address', 'phone', 'email' , 'working_hours']

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = ClinicAnnouncement
        fields = ['title', 'content', 'is_published']