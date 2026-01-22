

from django.template.response import TemplateResponse
from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Appointment
from .forms import ChangeTimeForm
from django.core.mail import send_mail
from django.conf import settings

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'doctor', 'date', 'time', 'approved', 'conflict_status', 'admin_actions']
    date_hierarchy = 'date'
    list_filter = ['date', 'doctor', 'approved']
    list_per_page = 20
    search_fields = ['doctor__name', 'name']

    def conflict_status(self, obj):
        if obj.has_conflict():
            return format_html('<span style="color:red;">Conflict</span>')
        return format_html('<span style="color:green;">No</span>')
    conflict_status.short_description = 'Conflict'

    def admin_actions(self, obj):
        approve_url = reverse('admin:approve-appointment', args=[obj.pk])
        change_url = reverse('admin:change-time', args=[obj.pk])
        return format_html(
            '<a class="button" style="margin-right: 5px;" href="{}">Approve</a>'
            '<a class="button" href="{}">Change Time</a>',
            approve_url,
            change_url
        )
    admin_actions.short_description = 'Actions'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('approve/<int:pk>/', self.admin_site.admin_view(self.approve_appointment), name='approve-appointment'),
            path('change-time/<int:pk>/', self.admin_site.admin_view(self.change_time), name='change-time'),
        ]
        return custom_urls + urls

    def approve_appointment(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.approved = True
        appointment.save()
        send_mail(
            subject="Appointment Approved",
            message=(
                f"Dear {appointment.name},\n\n"
                f"Your appointment with Dr. {appointment.doctor} on {appointment.date} at {appointment.time} has been approved.\n\n"
                "Thank you!"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[appointment.email],
            fail_silently=False,
        )
        self.message_user(request, f"Appointment for {appointment.name} approved successfully.", messages.SUCCESS)
        return redirect(reverse("admin:appointment_appointment_changelist")) 

    def change_time(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)

        if request.method == "POST":
            form = ChangeTimeForm(request.POST)
            if form.is_valid():
                appointment.time = form.cleaned_data['time']
                appointment.save()
                send_mail(
                    subject="Appointment Time Changed",
                    message=(
                        f"Dear {appointment.name},\n\n"
                        f"Your appointment with Dr. {appointment.doctor} has been rescheduled to {appointment.date} at {appointment.time}.\n\n"
                        "Thank you!"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[appointment.email],
                    fail_silently=False,
                )
                self.message_user(
                    request,
                    f"Time changed to {appointment.time} for {appointment.name}.",
                    messages.SUCCESS
                )
                return redirect(reverse("admin:appointment_appointment_changelist"))

        else:
            form = ChangeTimeForm(initial={"time": appointment.time})

        context = dict(
            self.admin_site.each_context(request),
            title=f"Change Time for {appointment.name}",
            form=form,
            appointment=appointment,
        )
        return TemplateResponse(request, "admin/change_time.html", context)