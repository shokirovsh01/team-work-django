from django.db.models.signals import post_save
from django.dispatch import receiver
from appointments.models import Appointment
from .models import Notification


@receiver(post_save, sender=Appointment)
def appointment_notification(sender, instance, created, **kwargs):
    date_str = instance.appointment_date.strftime("%d.%m.%Y в %H:%M") if instance.appointment_date else "указанное время"
    doc_name = instance.doctor.user.get_full_name() or instance.doctor.user.username
    patient_name = instance.patient.get_full_name() or instance.patient.username

    if created:
        if instance.doctor and instance.doctor.user:
            Notification.objects.create(
                recipient=instance.doctor.user,
                title="Новая запись на приём",
                message=f"Пациент {patient_name} записался к вам на консультацию: {date_str}."
            )
        Notification.objects.create(
            recipient=instance.patient,
            title="Запись на приём создана",
            message=f"Вы успешно записались к врачу {doc_name} на {date_str}. Статус: ожидает подтверждения врачом."
        )
    else:
        if instance.status == 'confirmed':
            Notification.objects.create(
                recipient=instance.patient,
                title="Запись подтверждена",
                message=f"Врач {doc_name} подтвердил ваш приём на {date_str}."
            )
        elif instance.status == 'cancelled':
            Notification.objects.create(
                recipient=instance.patient,
                title="Запись отменена",
                message=f"Запись к врачу {doc_name} на {date_str} была отменена."
            )
            if instance.doctor and instance.doctor.user:
                Notification.objects.create(
                    recipient=instance.doctor.user,
                    title="Запись отменена",
                    message=f"Запись пациента {patient_name} на {date_str} отменена."
                )
        elif instance.status == 'completed':
            Notification.objects.create(
                recipient=instance.patient,
                title="Консультация завершена",
                message=f"Ваш приём у врача {doc_name} завершён. Пожалуйста, поделитесь впечатлением и оставьте отзыв!"
            )
