from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from .models import Appointment,Doctor
from schedules.models import TimeSlot
from .forms import AppointmentBookForm
from django.forms import ValidationError

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
        appointment_date = form.cleaned_data.get('appointment_date')

        existing_appointment = Appointment.objects.filter(doctor=doctor,appointment_date=appointment_date,status__in=['pending','confirmed']).exists()

        if existing_appointment:
            form.add_error('appointment_date', 'Врач уже занят на это время.')
            return self.form_invalid(form)
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
        return redirect('appointments:my_appointments')

    
class AppointmentsAvailableView(LoginRequiredMixin,ListView):
    model = TimeSlot
    template_name = 'media2/available_slots.html'
    context_object_name = 'slots'

    def get_queryset(self):
        return TimeSlot.objects.filter(
            doctor_id=self.kwargs['doctor_id'],
            status='free',
            ).order_by('date','start_time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctor'] = get_object_or_404(Doctor,pk=self.kwargs['doctor_id']) 
        return context

class AppointmentUpdateView(LoginRequiredMixin,UpdateView):
    model = Appointment
    template_name = 'media2/appointment_update.html'
    fields = ['appointment_date']
    success_url = reverse_lazy('appointments:my_appointments')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['doctor'] = self.object.doctor
        return context

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user,status='pending')

class DoctorAppointmentsView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'media2/doctor_appointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        try:
            doctor = Doctor.objects.get(user=self.request.user)
            return Appointment.objects.filter(doctor=doctor).order_by('-appointment_date')
        except Doctor.DoesNotExist:
            if self.request.user.is_staff or self.request.user.is_superuser:
                return Appointment.objects.all().order_by('-appointment_date')
            return Appointment.objects.none()

class AppointmentConfirmView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if request.user.is_staff or request.user.is_superuser:
            appointment = get_object_or_404(Appointment, pk=pk)
        else:
            doctor = get_object_or_404(Doctor, user=request.user)
            appointment = get_object_or_404(Appointment, pk=pk, doctor=doctor)
        appointment.status = 'confirmed'
        appointment.save()
        return redirect('appointments:doctor_appointments')

class AppointmentCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if request.user.is_staff or request.user.is_superuser:
            appointment = get_object_or_404(Appointment, pk=pk)
        else:
            doctor = get_object_or_404(Doctor, user=request.user)
            appointment = get_object_or_404(Appointment, pk=pk, doctor=doctor)
        appointment.status = 'completed'
        appointment.save()
        return redirect('appointments:doctor_appointments')

    
    