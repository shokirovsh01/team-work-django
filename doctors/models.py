from django.db import models
from django.contrib.auth.models import User



class Specialization(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=50)    
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration=models.PositiveIntegerField()
    specialization  = models.ForeignKey(Specialization , on_delete=models.SET_NULL,null=True,blank=True,related_name='services')

    def __str__(self):
        return self.name



class Doctor(models.Model):
    user=models.OneToOneField(User,related_name='doctor_profile', on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization,on_delete=models.SET_NULL,null=True,related_name='doctors')
    services=models.ManyToManyField(Service,blank=True,related_name='doctors')
    bio=models.TextField()
    experience_years = models.PositiveIntegerField(default=0)
    photo = models.ImageField(upload_to='doctors/photos/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"







