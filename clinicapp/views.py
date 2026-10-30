from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView, ListView, CreateView

from accountsapp.models import PatientProfile
from accountsapp.roles import ClinicAdminRequiredMixin, StaffRequiredMixin, is_clinic_admin
from .forms import ClinicForm, AnnouncementForm
from .models import Clinic, ClinicAnnouncement



class ClinicDetailView(DetailView):
    template_name = 'media3/clinic_detail.html'

    def get_object(self, queryset=None):
        return Clinic.objects.first()

    def get_context_data(self, **kwargs):
        conten = super().get_context_data(**kwargs)
        conten['announcements'] = ClinicAnnouncement.objects.filter(is_published=True)[:5]
        return conten



class ClinicUpdateView(ClinicAdminRequiredMixin, UpdateView):
    form_class = ClinicForm
    template_name = 'media3/clinic_form.html'
    success_url = reverse_lazy('clinic_detail')

    def get_object(self, queryset=None):
        return Clinic.objects.first()


    
class PatientListView(StaffRequiredMixin, ListView):
    template_name = 'media3/patient_list.html'
    paginate_by = 20
    queryset = PatientProfile.objects.select_related('user')



class AnnouncementCreateView(ClinicAdminRequiredMixin, CreateView):
    form_class = AnnouncementForm
    template_name = 'media3/announcement_form.html'
    success_url = reverse_lazy('announcement_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.clinic = Clinic.objects.first()
        return super().form_valid(form)


class AnnouncementUpdateView(ClinicAdminRequiredMixin, UpdateView):
    model = ClinicAnnouncement
    form_class = AnnouncementForm
    template_name = 'media3/announcement_form.html'
    success_url = reverse_lazy('announcement_list')
    
    
class AnnouncementListView(ListView):
    template_name = 'media3/announcement_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = ClinicAnnouncement.objects.all()
        if not is_clinic_admin(self.request.user):
            qs = qs.filter(is_published=True)
        return qs
    
class AnnouncementDeleteView(ClinicAdminRequiredMixin, View):
    def post(self, request, pk):
        get_object_or_404(ClinicAnnouncement, pk=pk).delete()
        messages.success(request, 'Deleted!!!')
        return redirect('announcement_list')

