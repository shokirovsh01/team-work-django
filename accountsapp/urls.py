from django.urls import path
from .views import RegisterViews, CustomLoginView, ProfileEditView, ProfileView, activate
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

urlpatterns = [
    path('register/', RegisterViews.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile_edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('email-sent/', TemplateView.as_view(template_name='media3/email_sent.html'), name='email_sent'),
]