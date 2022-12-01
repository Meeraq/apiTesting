from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.template.loader import render_to_string


class Profile(models.Model):
    user_choice = [
        ('coach', 'coach'),
        ('admin', 'admin'),
        ('learner', 'learner'),
        ('finance', 'finance')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=50, choices=user_choice, default='coach')
    email = models.CharField(max_length=200, default="a@gmail.com")

    def __str__(self):
        return self.user.username


# coach Modal

class Coach(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, blank=True)
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, blank=True, default=" ")
    last_name = models.CharField(max_length=200, default=" ")
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    dob = models.DateField(blank=True, default="2000-01-01")
    gender = models.CharField(max_length=200, blank=True, default="NA")
    fee = models.IntegerField(blank=True, default="0")
    activeSince = models.DateField(blank=True, default="2000-01-01")
    isSlotBooked = models.BooleanField(default=False, blank=True)
    isActive = models.BooleanField(default=False, blank=True)
    meet_link = models.CharField(max_length=500, default='')

    def __str__(self):
        return self.first_name


# New coach model


class AdminRequest(models.Model):
    assigned_coach = models.ManyToManyField(Coach, related_name='Coach')
    confirmed_coach = models.ManyToManyField(
        Coach, related_name='confirmed_coach', blank=True)
    name = models.CharField(blank=True, max_length=200, default='Request -')
    isActive = models.BooleanField(default=True)
    expire_date = models.DateField(default="2022-09-10")
    end_date = models.DateField(default="2022-12-01")


class SlotForCoach(models.Model):
    start_time = models.CharField(blank=True, max_length=200, default="null")
    end_time = models.CharField(blank=True, max_length=200, default="null")
    date = models.DateField()
    request = models.ForeignKey(
        AdminRequest, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ConfirmedSlotsbyCoach(models.Model):
    coach_id = models.CharField(max_length=200)
    start_time = models.CharField(blank=True, max_length=200, default="null")
    end_time = models.CharField(blank=True, max_length=200, default="null")
    date = models.DateField()
    request_ID = models.CharField(max_length=200)
    SESSION_START_TIME = models.CharField(
        blank=True, max_length=200, default="null")
    SESSION_END_TIME = models.CharField(
        blank=True, max_length=200, default="null")
    SESSION_DATE = models.CharField(blank=True, max_length=200, default="null")
    COACH_NAME = models.CharField(blank=True, max_length=200, default="null")
    DESCRIPTION = models.CharField(blank=True, max_length=200, default="null")
    CC = models.CharField(blank=True, max_length=200, default="null")
    MEETING_LINK = models.CharField(blank=True, max_length=200, default=" ")
    is_confirmed = models.BooleanField(default=False)
    is_realeased = models.BooleanField(default=False)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "https://coach.meeraq.com/reset-password/" + \
        reset_password_token.key
    email_message = render_to_string("resetpasswordmail.html", {
                                     'url': email_plaintext_message})
    # create_random_user_accounts.delay(total)
    send_mail(
        # title:
        "Password Reset for {title}".format(title="Meeraq Slot Scheduler"),
        # message:
        email_plaintext_message,
        # from:0
        "info@meeraq.com",
        # to:
        [reset_password_token.user.email],
        html_message=email_message
    )


class Events(models.Model):
    name = models.CharField(max_length=200, default="Event")
    start_date = models.DateField(default="2022-09-09")
    end_date = models.DateField(default="2022-09-09")
    expire_date = models.DateField(default="2022-09-09")
    count = models.IntegerField(default=0)
    min_count = models.IntegerField(default=0, blank=True)
    link = models.CharField(max_length=200, default=" ", blank=True)
    _id = models.CharField(max_length=1000)
    coach = models.ManyToManyField(Coach)
    batch = models.CharField(max_length=200, blank=True, default=" ")
    is_expired = models.BooleanField(default=False, blank=True)
    is_delete = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.name


class LeanerConfirmedSlots(models.Model):
    name = models.CharField(max_length=200, default=" ")
    email = models.EmailField()
    phone_no = models.CharField(max_length=200)
    organisation = models.CharField(max_length=200, blank=True, default=" ")
    slot = models.ForeignKey(ConfirmedSlotsbyCoach,
                             null=True, on_delete=models.SET_NULL)
    event = models.ForeignKey(Events, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=200, blank=True, default='null')
    is_coach_joined = models.CharField(
        max_length=100, blank=True, default='null')
    is_learner_joined = models.CharField(
        max_length=100, blank=True, default='null')

    def __str__(self):
        return self.name


class DeleteConfirmedSlotsbyAdmin(models.Model):
    requested_person = models.CharField(max_length=200, default=" ")
    reason = models.CharField(max_length=200, default=" ")
    slot_id = models.CharField(max_length=200, default=" ")
    admin_name = models.CharField(max_length=200, default=" ")


class Learner(models.Model):
    first_name = models.CharField(max_length=200, default=" ")
    last_name = models.CharField(max_length=200, default=" ", blank=True)
    email = models.EmailField()
    batch = models.CharField(max_length=200, default=" ")
    phone = models.CharField(max_length=200, default=" ", blank=True)
    unique_check = models.CharField(max_length=200, default="null")
    course = models.CharField(max_length=200, default=" ", blank=True)


class Batch(models.Model):
    batch = models.CharField(max_length=200, default=" ", primary_key=True)


class ServiceApprovalData(models.Model):
    ref_id = models.CharField(max_length=100)
    fees = models.IntegerField(default="500")
    total_no_of_sessions = models.IntegerField(default=0)
    generated_date = models.DateField()
    generate_for_month = models.CharField(
        max_length=200, default=" ",  blank=True)
    generate_for_year = models.CharField(
        max_length=200, default=" ",  blank=True)
    is_approved = models.CharField(default="null", max_length=200, blank=True)
    invoice_no = models.CharField(max_length=200, default=" ",  blank=True)
    coach_id = models.ForeignKey(Coach, null=True, on_delete=models.SET_NULL)
    rejection_reason = models.CharField(
        max_length=200, default=" ",  blank=True)
    response_by_finance_date = models.DateField(
        default="2022-09-09", blank=True)
