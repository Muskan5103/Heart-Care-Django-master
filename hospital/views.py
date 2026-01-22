from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import Slider, Service, Doctor, Faq, Gallery
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings
from .models import ContactMessage  # ✅ import your model
import requests
from django.views.generic import ListView
from django.db.models import Q
from .models import Faq

class HomeView(ListView):
    template_name = 'hospital/index.html'
    queryset = Service.objects.all()
    context_object_name = 'services'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['sliders'] = Slider.objects.all()
        context['experts'] = Doctor.objects.all()
        return context


class ServiceListView(ListView):
    queryset = Service.objects.all()
    template_name = "hospital/services.html"


class ServiceDetailView(DetailView):
    queryset = Service.objects.all()
    template_name = "hospital/service_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.object
        context["services"] = Service.objects.all()
        context["doctors"] = service.doctors.all()
        return context


class DoctorListView(ListView):
    template_name = 'hospital/team.html'
    queryset = Doctor.objects.all()
    paginate_by = 8


class DoctorDetailView(DetailView):
    template_name = 'hospital/team-details.html'
    queryset = Doctor.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctors"] = Doctor.objects.all()
        return context


# class FaqListView(ListView):
#     template_name = 'hospital/faqs.html'
#     queryset = Faq.objects.all()
class FaqListView(ListView):
    model = Faq
    template_name = 'hospital/faqs.html'
    context_object_name = 'faqs'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(question__icontains=query) | Q(answer__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class GalleryListView(ListView):
    template_name = 'hospital/gallery.html'
    queryset = Gallery.objects.all()
    paginate_by = 9



# class ContactView(TemplateView):
#     template_name = "hospital/contact.html"

#     def post(self, request, *args, **kwargs):
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         subject = request.POST.get('subject') or "Heartcare Contact"
#         message = request.POST.get('message')

#         if name and message and email and phone:
#             # ✅ Save to the database
#             ContactMessage.objects.create(
#                 name=name,
#                 email=email,
#                 phone=phone,
#                 subject=subject,
#                 message=message
#             )

#             # ✅ Send email as before
#             send_mail(
#                 f"{subject} - {phone}",
#                 message,
#                 email,
#                 ['expelmahmud@gmail.com'],
#                 fail_silently=False,
#             )

#             messages.success(request, "Email has been sent and saved successfully.")
#         else:
#             messages.error(request, "Please fill in all required fields.")

#         return redirect('contact')



class ContactView(TemplateView):
    template_name = "hospital/contact.html"

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject') or "Heartcare Contact"
        message = request.POST.get('message')

        if name and message and email and phone:
            # ✅ Save to the database
            obj = ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message
            )

            # ✅ Send message to Admin
            send_mail(
                f"{subject} - {phone}",
                message,
                email,
                ['expelmahmud@gmail.com'],   # admin email
                fail_silently=False,
            )

            # ✅ Send acknowledgement Email to User
            ack_subject = "Thank you for contacting Heart Care"
            ack_message = (
                f"Dear {obj.name},\n\n"
                f"We have received your message regarding '{obj.subject}'. "
                f"Our team will get back to you soon.\n\nBest Regards,\nHeart Care Hospital"
            )
            try:
                send_mail(
                    ack_subject,
                    ack_message,
                    settings.EMAIL_HOST_USER,   # sender email
                    [obj.email],                # user email
                    fail_silently=False,
                )
            except Exception as e:
                print("User email sending failed:", e)

            # ✅ Send acknowledgement SMS to User
            try:
                url = "https://www.fast2sms.com/dev/bulkV2"
                payload = {
                    "sender_id": "TXTIND",
                    "message": f"Hello {obj.name}, thanks for contacting Heart Care Hospital. "
                               f"We received your query about '{obj.subject}'. Our team will reply soon.",
                    "route": "q",
                    "numbers": obj.phone,   # must be 10-digit Indian number
                }
                headers = {
                    "authorization": settings.FAST2SMS_API_KEY,
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Cache-Control": "no-cache"
                }
                response = requests.post(url, data=payload, headers=headers)
                print("SMS Response:", response.json())
            except Exception as e:
                print("SMS sending failed:", e)

            messages.success(request, "Your message has been sent. You will receive acknowledgement shortly.")
        else:
            messages.error(request, "Please fill in all required fields.")

        return redirect('contact')
