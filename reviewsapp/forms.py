from django import forms
from .models import DoctorReview

class ReviewForm(forms.ModelForm):
    class Meta:
        model = DoctorReview
        fields = ['rating', 'comment']
        labels = {'rating': 'Оценка', 'comment': 'Комментарий'}