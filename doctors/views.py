from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import datetime
from .models import *

def doctor_list(request):
    q = request.GET.get('q', '').strip()
    specialization_id = request.GET.get('specialization', '')
    doctors = Doctor.objects.all().select_related('user', 'specialization')
    if not request.user.is_staff:
        doctors = doctors.filter(is_active=True)
    if q:
        doctors = doctors.filter(
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q) |
            Q(bio__icontains=q) |
            Q(specialization__name__icontains=q)
        )
    if specialization_id and specialization_id.isdigit():
        doctors = doctors.filter(specialization_id=int(specialization_id))
    specializations = Specialization.objects.all()
    return render(request, 'doctors/doctor_list.html', {
        'doctors': doctors,
        'specializations': specializations,
        'q': q,
        'selected_specialization': specialization_id,
    })

def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor.objects.select_related('user', 'specialization'), pk=pk)
    schedules = doctor.schedules.all().order_by('weekday')
    today = datetime.now().date()
    slots = doctor.slots.filter(date__gte=today, status='free').order_by('date', 'start_time')[:15]
    days_off = doctor.days_off.filter(date__gte=today).order_by('date')
    is_owner = hasattr(request.user, 'doctor_profile') and request.user.doctor_profile == doctor
    can_edit = request.user.is_staff or is_owner
    return render(request, 'doctors/doctor_detail.html', {
        'doctor': doctor,
        'schedules': schedules,
        'slots': slots,
        'days_off': days_off,
        'can_edit': can_edit,
    })

def doctor_create(request):
    if not request.user.is_staff:
        return HttpResponse('<h1>Доступ запрещен (только администратор)</h1>', status=403)
    if request.method == 'POST':
        data = request.POST
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        email = data.get('email', '').strip()
        specialization_id = data.get('specialization', '')
        experience_years = data.get('experience_years', 0)
        phone = data.get('phone', '')
        bio = data.get('bio', '')
        is_active = 'is_active' in data
        photo = request.FILES.get('photo')

        if not first_name or not last_name or not username or not password:
            return render(request, 'doctors/doctor_form.html', {
                'error': 'Заполните обязательные поля: имя, фамилия, логин и пароль.',
                'specializations': Specialization.objects.all(),
                'services': Service.objects.all(),
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'doctors/doctor_form.html', {
                'error': 'Пользователь с таким логином уже существует.',
                'specializations': Specialization.objects.all(),
                'services': Service.objects.all(),
            })
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        spec = Specialization.objects.filter(pk=specialization_id).first() if specialization_id else None
        doctor = Doctor.objects.create(
            user=user,
            specialization=spec,
            experience_years=int(experience_years) if experience_years else 0,
            phone=phone,
            bio=bio,
            photo=photo,
            is_active=is_active
        )
        services = data.getlist('services')
        if services:
            doctor.services.set(Service.objects.filter(id__in=services))
        return redirect('doctor_detail', pk=doctor.pk)

    return render(request, 'doctors/doctor_form.html', {
        'specializations': Specialization.objects.all(),
        'services': Service.objects.all(),
    })

def doctor_edit(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    is_owner = hasattr(request.user, 'doctor_profile') and request.user.doctor_profile == doctor
    if not (request.user.is_staff or is_owner):
        return HttpResponse('<h1>Доступ запрещен</h1>', status=403)

    if request.method == 'POST':
        data = request.POST
        doctor.user.first_name = data.get('first_name', '').strip()
        doctor.user.last_name = data.get('last_name', '').strip()
        doctor.user.email = data.get('email', '').strip()
        doctor.user.save()

        spec_id = data.get('specialization', '')
        doctor.specialization = Specialization.objects.filter(pk=spec_id).first() if spec_id else None
        exp = data.get('experience_years', 0)
        doctor.experience_years = int(exp) if exp else 0
        doctor.phone = data.get('phone', '').strip()
        doctor.bio = data.get('bio', '').strip()
        if 'photo' in request.FILES:
            doctor.photo = request.FILES['photo']
        doctor.is_active = 'is_active' in data
        doctor.save()

        services = data.getlist('services')
        doctor.services.set(Service.objects.filter(id__in=services))
        return redirect('doctor_detail', pk=doctor.pk)

    return render(request, 'doctors/doctor_form.html', {
        'doctor': doctor,
        'specializations': Specialization.objects.all(),
        'services': Service.objects.all(),
    })

def doctor_delete(request, pk):
    if not request.user.is_staff:
        return HttpResponse('<h1>Доступ запрещен (только администратор)</h1>', status=403)
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.is_active = False
        doctor.save()
        return redirect('doctor_list')
    return render(request, 'doctors/doctor_confirm_delete.html', {'doctor': doctor})

def specialization_list(request):
    if request.method == 'POST':
        if not request.user.is_staff:
            return HttpResponse('<h1>Доступ запрещен</h1>', status=403)
        data = request.POST
        action = data.get('action')

        if action == 'add_specialization':
            name = data.get('name', '').strip()
            description = data.get('description', '').strip()
            if name:
                Specialization.objects.create(name=name, description=description)
            return redirect('specialization_list')

        elif action == 'add_service':
            name = data.get('name', '').strip()
            description = data.get('description', '').strip()
            price = data.get('price', 0)
            duration = data.get('duration', 30)
            spec_id = data.get('specialization_id')
            spec = Specialization.objects.filter(pk=spec_id).first()
            if name and spec:
                Service.objects.create(
                    name=name,
                    description=description,
                    price=price,
                    duration=int(duration) if duration else 30,
                    specialization=spec
                )
            return redirect('specialization_list')


    specializations = Specialization.objects.all().prefetch_related('services', 'doctors')
    return render(request, 'doctors/specialization_list.html', {
        'specializations': specializations,
    })
