from django.db import models
from django.conf import settings

class Clinic(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)
    email = models.EmailField('email', blank=True)
    working_hours = models.CharField('work_hour', max_length=200, blank=True)

    def __str__(self):
        return self.name

class ClinicAnnouncement(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title 