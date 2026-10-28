from django.db import models
from django.contrib.auth.models import User


class Clinic(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.name


class ClinicAnnouncement(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title