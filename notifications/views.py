from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from .models import Notification

class NotificationListView(LoginRequiredMixin,ListView):
    model = Notification
    template_name = 'media2/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

class NotificationReadView(LoginRequiredMixin,View):
    def post(self, request, pk):
        notification = get_object_or_404(Notification,pk=pk,recipient=request.user)
        notification.is_read = True
        notification.save()
        return redirect('notifications:notification_list')

    