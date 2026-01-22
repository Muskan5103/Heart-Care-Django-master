from django.db import models
from hospital.models import Doctor
from django.utils import timezone

TIME_CHOICES = [
    ("09:00 AM", "09:00 AM"), ("09:30 AM", "09:30 AM"),
    ("10:00 AM", "10:00 AM"), ("10:30 AM", "10:30 AM"),
    ("11:00 AM", "11:00 AM"), ("11:30 AM", "11:30 AM"),
    ("12:00 PM", "12:00 PM"),
    ("02:00 PM", "02:00 PM"), ("02:30 PM", "02:30 PM"),
    ("03:00 PM", "03:00 PM"), ("03:30 PM", "03:30 PM"),
    ("04:00 PM", "04:00 PM"), ("04:30 PM", "04:30 PM")
]
class Appointment(models.Model):
    time = models.CharField(max_length=20, choices=TIME_CHOICES)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField(default=timezone.now)
    # time = models.CharField(choices=time, max_length=10)
    note = models.TextField(blank=True, null=True)
    approved = models.BooleanField(default=False)

    def has_conflict(self):
        return Appointment.objects.filter(
            doctor=self.doctor,
            date=self.date,
            time=self.time
        ).exclude(id=self.id).exists()

    def __str__(self):
        return f"{self.name}-{self.doctor.name}"
