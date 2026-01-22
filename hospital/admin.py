# from django.contrib import admin
# from .models import (Slider, Service, Item, Doctor, Expertize, Faq, Gallery,ContactMessage)

# admin.site.register(Slider)
# # admin.site.register(Service)

# admin.site.register(Item)
# admin.site.register(Doctor)
# admin.site.register(Expertize)
# admin.site.register(Faq)
# admin.site.register(Gallery)
# admin.site.register(ContactMessage)
# @admin.register(Service)
# class ServiceAdmin(admin.ModelAdmin):
#     list_display = ("title",)
#     filter_horizontal = ("doctors",) 

from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
import requests
from .models import (Slider, Service, Item, Doctor, Expertize, Faq, Gallery, ContactMessage)

# Register models normally
admin.site.register(Slider)
admin.site.register(Item)
admin.site.register(Doctor)
admin.site.register(Expertize)
admin.site.register(Faq)
admin.site.register(Gallery)

# -------- Service Admin ----------
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title",)
    filter_horizontal = ("doctors",)


# -------- ContactMessage Admin ----------
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # -------- Email Acknowledgement ----------
        subject = "Thank you for contacting Heart Care"
        message = (
            f"Dear {obj.name},\n\n"
            f"We have received your message regarding '{obj.subject}'. "
            f"Our team will get back to you soon.\n\nBest Regards,\nHeart Care Hospital"
        )

        try:
            send_mail(
                subject,
                message,
                None,  # Uses DEFAULT_FROM_EMAIL
                [obj.email],
                fail_silently=False,
            )
        except Exception as e:
            print("Email sending failed:", e)

        # -------- SMS Acknowledgement (Fast2SMS) ----------
        try:
            url = "https://www.fast2sms.com/dev/bulkV2"
            payload = {
                "sender_id": "TXTIND",
                "message": f"Hello {obj.name}, thanks for contacting Heart Care Hospital. "
                           f"We received your query about '{obj.subject}'. Our team will reply soon.",
                "route": "q",
                "numbers": obj.phone,  # 10-digit mobile number
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
