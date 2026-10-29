
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from datetime import datetime
from doctors.models import Doctor
from .models import WorkSchedule, TimeSlot, DayOff

def _check_doctor_permission(request, doctor):
    if request.user.is_staff or doctor.user == request.user:
        return True
    return False

def doctor_schedule(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    can_manage = _check_doctor_permission(request, doctor)

    if request.method == 'POST':
        if not can_manage:
            return HttpResponse('<h1>Доступ запрещен</h1>', status=403)
        
        data = request.POST
        action = data.get('action')

        if action == 'save_schedule':
            weekday = int(data.get('weekday'))
            start_time = data.get('start_time')
            end_time = data.get('end_time')
            slot_duration = int(data.get('slot_duration', 30))

            WorkSchedule.objects.update_or_create(
                doctor=doctor,
                weekday=weekday,
                defaults={
                    'start_time': start_time,
                    'end_time': end_time,
                    'slot_duration': slot_duration
                }
            )
            return redirect('doctor_schedule', doctor_id=doctor.id)

        elif action == 'delete_schedule':
            weekday = int(data.get('weekday'))
            WorkSchedule.objects.filter(doctor=doctor, weekday=weekday).delete()
            return redirect('doctor_schedule', doctor_id=doctor.id)

    schedules = doctor.schedules.all().order_by('weekday')
    today = datetime.now().date()
    slots = doctor.slots.filter(date__gte=today).order_by('date', 'start_time')
    days_off = doctor.days_off.filter(date__gte=today).order_by('date')

    configured_weekdays = {s.weekday for s in schedules}
    weekday_choices = [
        (num, name, num in configured_weekdays)
        for num, name in WorkSchedule.WEEKDAYS
    ]

    return render(request, 'schedules/doctor_schedule.html', {
        'doctor': doctor,
        'schedules': schedules,
        'slots': slots,
        'days_off': days_off,
        'weekday_choices': weekday_choices,
        'can_manage': can_manage,
    })

def days_off(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    if not _check_doctor_permission(request, doctor):
        return HttpResponse('<h1>Доступ запрещен</h1>', status=403)

    error = None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            date_str = request.POST.get('date', '').strip()
            reason = request.POST.get('reason', '').strip()

            if not date_str:
                error = 'Укажите дату выходного'
            else:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                if date < datetime.now().date():
                    error = 'Нельзя назначить выходной в прошедшую дату'
                elif DayOff.objects.filter(doctor=doctor, date=date).exists():
                    error = 'Этот день уже добавлен в выходные'
                else:
                    DayOff.objects.create(doctor=doctor, date=date, reason=reason)
                    # Удаляем свободные слоты на этот день (согласно ТЗ)
                    doctor.slots.filter(date=date, status='free').delete()
                    return redirect('days_off', doctor_id=doctor.id)

        elif action == 'delete':
            day_off_id = request.POST.get('day_off_id')
            DayOff.objects.filter(id=day_off_id, doctor=doctor).delete()
            return redirect('days_off', doctor_id=doctor.id)

    today = datetime.now().date()
    days_off_list = doctor.days_off.filter(date__gte=today).order_by('date')

    return render(request, 'schedules/days_off.html', {
        'doctor': doctor,
        'days_off': days_off_list,
        'error': error,
    })


def slot_create(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    if not _check_doctor_permission(request, doctor):
        return HttpResponse('<h1>Доступ запрещен</h1>', status=403)

    error = None

    if request.method == 'POST':
        date_str = request.POST.get('date', '').strip()
        start_time_str = request.POST.get('start_time', '').strip()
        end_time_str = request.POST.get('end_time', '').strip()

        if not date_str or not start_time_str or not end_time_str:
            error = 'Заполните все поля'
        else:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()

            if date < datetime.now().date():
                error = 'Нельзя создать слот на прошедшую дату'
            elif start_time >= end_time:
                error = 'Время окончания должно быть позже времени начала'
            elif DayOff.objects.filter(doctor=doctor, date=date).exists():
                error = 'В этот день у врача выходной'
            # Предотвращение дублирующихся и пересекающихся слотов:
            # Новый слот пересекается со старым, если: start_time < old.end_time AND end_time > old.start_time
            elif TimeSlot.objects.filter(
                doctor=doctor,
                date=date,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exists():
                error = 'На это время у врача уже существует или пересекается другой слот'
            else:
                TimeSlot.objects.create(
                    doctor=doctor,
                    date=date,
                    start_time=start_time,
                    end_time=end_time,
                    status='free'
                )
                return redirect('doctor_schedule', doctor_id=doctor.id)

    return render(request, 'schedules/slot_form.html', {
        'doctor': doctor,
        'error': error,
    })
