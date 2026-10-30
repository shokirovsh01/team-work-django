from django.urls import path
from .views import ReviewCreateView, ReviewUpdateView, ReviewDeleteView, StatsView

urlpatterns = [
    path('appointment/<int:pk>/', ReviewCreateView.as_view(), name='review_create'),
    path('<int:pk>/edit/', ReviewUpdateView.as_view(), name='review_edit'),
    path('<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
    path('stats/', StatsView.as_view(), name='clinic_stats'),
]