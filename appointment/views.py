from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from hospital.models import Doctor
from .models import Appointment


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        doctor_id = request.GET.get('doctor_id')
        context = {
            'doctors': Doctor.objects.all(),
            'selected_doctor_id': int(doctor_id) if doctor_id else None,
            'time_slots': [
                "09:00 AM", "09:30 AM", "10:00 AM", "10:30 AM",
                "11:00 AM", "11:30 AM", "12:00 PM",
                "02:00 PM", "02:30 PM", "03:00 PM", "03:30 PM",
                "04:00 PM", "04:30 PM"
            ]
        }
        return render(request, "appointment/index.html", context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')
        time = request.POST.get('time')
        note = request.POST.get('note')
        if doctor_id:
            doctor = get_object_or_404(Doctor, id=doctor_id)

        if(name and phone and email and doctor and date and time):
            Appointment.objects.create(
                name=name, phone=phone, email=email, doctor=doctor, date=date, time=time, note=note)
            messages.success(request,'Appointment done successfully')
        return redirect('appointment')


def approve_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    appointment.approved = True
    appointment.save()
    messages.success(request, f"Appointment for {appointment.name} approved.")
    return redirect('/admin/appointment/appointment/')

def change_time_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)

    # Your defined time slots
    TIME_SLOTS = [
        "09:00 AM", "09:30 AM", "10:00 AM", "10:30 AM",
        "11:00 AM", "11:30 AM", "12:00 PM",
        "02:00 PM", "02:30 PM", "03:00 PM", "03:30 PM",
        "04:00 PM", "04:30 PM"
    ]

    # Get already booked time slots for this doctor on the same date (excluding current appointment)
    booked_times = Appointment.objects.filter(
        doctor=appointment.doctor,
        date=appointment.date
    ).exclude(id=appointment.id).values_list('time', flat=True)

    try:
        current_index = TIME_SLOTS.index(appointment.time)
    except ValueError:
        current_index = -1

    # Try to find the next available time slot
    new_time = None
    for i in range(current_index + 1, len(TIME_SLOTS)):
        if TIME_SLOTS[i] not in booked_times:
            new_time = TIME_SLOTS[i]
            break

    if new_time:
        appointment.time = new_time
        appointment.save()
        messages.success(request, f"Time changed to {new_time}.")
    else:
        messages.warning(request, "No available later time slots on this day.")

    return redirect('/admin/appointment/appointment/')