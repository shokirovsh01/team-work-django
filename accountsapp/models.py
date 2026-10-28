from django.db import models
from django.contrib.auth.models import User

class PatientProfile(models.Model):
    USER_ROLES = (
        ('doctor', 'Доктор'),
        ('patient', 'Пациент'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='patient')
    phone = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(auto_now=True, blank=True, null=True)
    avatar = models = models.ImageField(upload_to = 'avatar/', blank = True, null = True)

    def __str__(self):
        return self.user.username

