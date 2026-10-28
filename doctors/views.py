<<<<<<< HEAD
from django.shortcuts import render

# Create your views here.
=======
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Doctor
from .forms import DoctorForm


def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            doctor = form.save()
            messages.success(request, f"Врач {doctor} успешно добавлен!")
            return redirect('doctors:doctor_edit', pk=doctor.pk)
    else:
        form = DoctorForm()

    return render(request, 'doctors/doctor_form.html', {'form': form})


def doctor_edit(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)

    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, f"Профиль врача {doctor} обновлен!")
            return redirect('doctors:doctor_edit', pk=doctor.pk)
    else:
        form = DoctorForm(instance=doctor)

    return render(request, 'doctors/doctor_form.html', {'form': form, 'doctor': doctor})
>>>>>>> origin/behruz
