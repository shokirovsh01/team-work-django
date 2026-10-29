from django.urls import path
from .views import RegisterViews, CustomLoginView, ProfileEditView, ProfileView
urlpatterns = [
    path('register/', RegisterViews.as_view(), name='register'),
]