from django.urls import path
from .views import *

urlpatterns = [
    path('', doctor_list, name='doctor_list'),
    path('<int:pk>/', doctor_detail, name='doctor_detail'),
    path('create/', doctor_create, name='doctor_create'),
    path('<int:pk>/edit/', doctor_edit, name='doctor_edit'),
    path('<int:pk>/delete/', doctor_delete, name='doctor_delete'),
    path('specializations/', specialization_list, name='specialization_list'),
]
