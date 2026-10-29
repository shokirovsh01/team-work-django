from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from .models import PatientProfile
from .forms import PatientRegistrationForm, PatientProfileForm
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()


class RegisterViews(CreateView):
    form_class = PatientRegistrationForm
    template_name = 'media3/register.html'
    success_url = reverse_lazy('email_send')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        self.object = user

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_url = self.request.build_absolute_uri(
            reverse('activate', kwargs={'uidb64': uid, 'token': token})
        )

        send_mail(
            subject='Email confirmation',
            message=(f'Hello {user.username}\n'
                     f'Click here to activate your account: {verification_url}'),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return HttpResponseRedirect(self.get_success_url())


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')

    return HttpResponse('<h1>Activation link is invalid!</h1>', status=400)

class CustomLoginView(LoginView):
    template_name = 'media3/login.html'
    redirect_authenticated_user = True

    

class ProfileView(LoginRequiredMixin, DetailView):
    model = PatientProfile
    template_name = 'media3/profile.html'

    def get_object(self, queryset=None):
        profile, created = PatientProfile.objects.get_or_create(user=self.request.user)
        return profile

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = PatientProfile
    form_class = PatientProfileForm
    template_name = 'media3/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        profile, created = PatientProfile.objects.get_or_create(user=self.request.user)
        return profile
from django.contrib.auth import logout 

def logout_view(request):
    logout(request)
    return redirect('login')
