from django.contrib import admin
from .models import Specialization, Service, Doctor


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'price', 'duration')
    list_filter = ('specialization',)
    search_fields = ('name',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'specialization', 'experience_years', 'is_active')
    list_filter = ('specialization', 'is_active')
<<<<<<< HEAD
    search_fields = ('user__first_name', 'user__last_name')
    filter_horizontal = ('services',)  
=======
    search_fields = ('user__first_name', 'user__last_name')  
>>>>>>> origin/behruz
