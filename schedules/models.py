from django.db import models
from doctors.models import Doctor

class WorkSchedule(models.Model):
    WEEKDAYS = [
        (0, 'Понедельник'), (1, 'Вторник'), (2, 'Среда'),
        (3, 'Четверг'), (4, 'Пятница'), (5, 'Суббота'), (6, 'Воскресенье'),
    ]
    doctor=models.ForeignKey(Doctor,related_name='schedules', on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=WEEKDAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_duration = models.PositiveIntegerField(default=30)

    class Meta:
        unique_together = ('doctor', 'weekday')

    def __str__(self):
        return f"{self.doctor} — {self.get_weekday_display()}"

class TimeSlot(models.Model):
    STATUS_FREE = 'free'
    STATUS_BOOKED = 'booked'
    STATUS_CHOICES = [(STATUS_FREE, 'Свободен'),(STATUS_BOOKED, 'Занят'),]
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_FREE)

    def __str__(self):
        return f"{self.doctor} | {self.date} {self.start_time}–{self.end_time} [{self.status}]"

class DayOff(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='days_off')
    date = models.DateField()
    reason = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('doctor', 'date')

    def __str__(self):
        return f"{self.doctor} — выходной {self.date}"

