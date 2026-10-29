from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from .models import Appointment,Doctor
from .forms import AppointmentBookForm

class MyAppointmentsView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'media2/my_appointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user).select_related('doctor', 'doctor__user').order_by('-appointment_date')


class AppointmentBookView(LoginRequiredMixin, CreateView):
    model = Appointment
    template_name = 'media2/appointment_form.html'
    fields = ['appointment_date']
    success_url = reverse_lazy('appointments:my_appointments')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctor'] = get_object_or_404(Doctor, pk=self.kwargs['doctor_id'])
        return context

    def form_valid(self, form):
        doctor = get_object_or_404(Doctor, pk=self.kwargs['doctor_id'])
        form.instance.doctor = doctor
        form.instance.patient = self.request.user
        return super().form_valid(form)


class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'media2/appointment_detail.html'
    context_object_name = 'appointment'


class AppointmentCancelView(LoginRequiredMixin, View):
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk, patient=request.user)
        appointment.status = 'cancelled'
        appointment.save()
        return redirect('my_appointments')

    
class AppointmentsAvailableView(LoginRequiredMixin,ListView):
    model = Doctor
    template_name = 'media2/doctor_appointments.html'
    context_object_name = 'doctor'

    # def get_queryset(self):
    #     return Doctor.objects.filter()
