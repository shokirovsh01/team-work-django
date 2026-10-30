from django.urls import path
from .views import ClinicDetailView, ClinicUpdateView, PatientListView, AnnouncementListView, AnnouncementCreateView, AnnouncementDeleteView

urlpatterns = [
    path('clinic/', ClinicDetailView.as_view(), name='clinic_detail'),
    path('clinic_update/', ClinicUpdateView.as_view(), name='clinic_edit'),
    path('patients/', PatientListView.as_view(), name='patient_list'),
    path('announcements/', AnnouncementListView.as_view(), name='announcement_list'),
    path('announcements_create/', AnnouncementCreateView.as_view(), name='announcement_create'),
    path('announcements_delete/<int:pk>/', AnnouncementDeleteView.as_view(), name='announcement_delete'),
]