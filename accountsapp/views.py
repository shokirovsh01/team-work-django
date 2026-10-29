from django.shortcuts import render
from django.contrib.auth.models import User
from .models import PatientProfile
from .forms import PatientRegistrationForm, PatientProfileForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView



class RegisterViews(CreateView):
    form_class = PatientRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

class ProfileView(LoginRequiredMixin, DetailView):
    model = PatientProfile
    template_name = 'accounts/profile_edit.html'

    def get_object(self):
        return self.request.user.patientprofile

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = PatientProfile
    form_class = PatientProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.patientprofile
    