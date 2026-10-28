from django.urls import path
<<<<<<< HEAD
urlpatterns = []
=======
from . import views

app_name = 'doctors'

urlpatterns = [
    path('create/', views.doctor_create, name='doctor_create'),
    path('<int:pk>/edit/', views.doctor_edit, name='doctor_edit'),
]
>>>>>>> origin/behruz
