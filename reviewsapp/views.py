from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from appointments.models import Appointment
from .forms import ReviewForm
from .models import DoctorReview
from django.views import View



class ReviewCreateView(LoginRequiredMixin, CreateView):
    form_class = ReviewForm
    template_name = 'media3/review_form.html'
    success_url = reverse_lazy('doctor_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.appointment = get_object_or_404(
            Appointment,
            pk=kwargs['pk'],
            patient=request.user,
            status='completed',
        )
        if DoctorReview.objects.filter(appointment=self.appointment).exists():
            messages.error(request, 'Отзыв на этот приём уже оставлен.')
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointment'] = self.appointment
        return context

    def form_valid(self, form):
        form.instance.appointment = self.appointment
        form.instance.patient = self.request.user
        form.instance.doctor = self.appointment.doctor
        messages.success(self.request, 'Thank you for review!')
        return super().form_valid(form)



class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ReviewForm
    template_name = 'media3/review_form.html'

    def get_queryset(self):
        return DoctorReview.objects.filter(patient=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointment'] = self.object.appointment
        return context

    def get_success_url(self):
        if self.object.doctor_id:
            return f'/doctors/{self.object.doctor_id}/'
        return reverse_lazy('doctor_list')

    def form_valid(self, form):
        messages.success(self.request, 'Updated')
        return super().form_valid(form)


class ReviewDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        review = get_object_or_404(DoctorReview, pk=pk, patient=request.user)
        doctor_id = review.doctor_id
        review.delete()
        messages.success(request, 'Deleted')
        if doctor_id:
            return redirect(f'/doctors/{doctor_id}/')
        return redirect('doctor_list')