import string
from celery import shared_task
from .models import SentEmail
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.core.mail import EmailMessage
from django.conf import settings


@shared_task
def add(a, b):
    print(a + b)


@shared_task
def send_email_to_recipients(id):
    try:
        sent_email = SentEmail.objects.get(id=id)
        if sent_email.status == "pending":
            for recipient in sent_email.recipients:
                recipient_name = recipient["name"]
                recipient_email = recipient["email"]
                email_content = sent_email.template.template_data.replace(
                    "{{learnerName}}", recipient_name
                )
                email_message_learner = render_to_string(
                    "default.html",
                    {
                        "email_content": mark_safe(email_content),
                        "email_title": "hello",
                        "subject": sent_email.subject,
                    },
                )
                email = EmailMessage(
                    sent_email.subject,
                    email_message_learner,
                    settings.DEFAULT_FROM_EMAIL,
                    [recipient_email],
                )
                email.content_subtype = "html"
                email.send()
                print(
                    "Email sent to:", recipient_email, "for recipient:", recipient_name
                )
            sent_email.status = "completed"
            sent_email.save()
            return "success"
        return "error: sent email is not pending"
    except:
        print("error")
        return "error: sent email not found "
