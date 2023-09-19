import string
from celery import shared_task
from .models import SentEmail, Events, Learner, LeanerConfirmedSlots, UserToken
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
import json
from api.views import refresh_microsoft_access_token


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


@shared_task
def send_event_link_to_learners(id):
    print("success")
    event = Events.objects.get(id=id)
    batch = event.batch
    learners = Learner.objects.filter(batch=batch)
    learners_with_no_sessions = []
    for learner in learners:
        sessions = LeanerConfirmedSlots.objects.filter(email=learner.email, event=event)
        if len(sessions) == 0:
            learners_with_no_sessions.append(learner.email)
    # print(learner_emails, type(learner_emails))
    # learner_emails_array = json.loads(learner_emails)
    for learner_mail in learners_with_no_sessions:
        try:
            email_message = render_to_string(
                "seteventlink.html",
                {"event_link": event.link},
            )
            send_mail(
                "Event link to join sessions on  {title}".format(title="Meeraq"),
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [learner_mail],
                html_message=email_message,
            )
        except Exception as e:
            print("Failed to send to ", learner_mail)
            pass


@shared_task
def refresh_user_tokens():
    users = UserToken.objects.filter(account_type="microsoft")
    for user in users:
        refresh_microsoft_access_token(user)
        print(f"token refresh for {user.user_mail}")
