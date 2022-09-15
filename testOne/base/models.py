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
        ('faculty', 'faculty')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=50, choices=user_choice, default='coach')
    email = models.CharField(max_length=200, default="a@gmail.com")

    def __str__(self):
        return self.user.username


# class CourseCategorys(models.Model):
#     courseCategoryName = models.CharField(max_length=200)

#     def __str__(self):
#         return self.courseCategoryName


# Courses Model
# class Courses(models.Model):
#     Name = models.CharField(max_length=200)
#     category = models.ForeignKey(
#         CourseCategorys, null=True, on_delete=models.SET_NULL)
#     created = models.DateTimeField(auto_now_add=True)
#     course_id = models.CharField(max_length=200, default='0000')
#     isActive = models.BooleanField(default=False)

#     def __str__(self):
#         return self.Name

# batch Modal


# class Batch(models.Model):
#     StartDate = models.DateField(blank=True, default="2000-01-01")
#     Name = models.CharField(max_length=200)
#     Faculty = models.CharField(max_length=200)
#     Fees = models.CharField(max_length=200)
#     Frequency = models.CharField(max_length=200)
#     NoOfSessions = models.IntegerField()
#     course = models.ForeignKey(Courses, null=True, on_delete=models.SET_NULL)
#     isActive = models.BooleanField(default=False)
#     duration = models.IntegerField(default=30)

#     def __str__(self):
#         return self.Name


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


# # Faculty Modal

# class Faculty(models.Model):
#     user = models.OneToOneField(Profile, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200)
#     email = models.CharField(max_length=200)
#     phone = models.CharField(max_length=200)
#     dob = models.DateField(blank=True, default="2000-01-01")
#     gender = models.CharField(max_length=200, blank=True)
#     fee = models.IntegerField(blank=True, default="6000")
#     activeSince = models.DateField(blank=True, default="2000-01-01")
#     isActive = models.BooleanField(default=False, blank=True)
#     password = models.CharField(max_length=50, default='Nish@@nt111')

#     def __str__(self):
#         return self.name


# # Learner Modal

# class Learners(models.Model):
#     user = models.OneToOneField(Profile, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200)
#     email = models.CharField(max_length=100)
#     phone = models.CharField(max_length=1000, default="7880647282")
#     company = models.CharField(max_length=100, blank=True, default="000")
#     industry = models.CharField(max_length=100, blank=True, default="000")
#     designation = models.CharField(max_length=100, blank=True, default="000")
#     dob = models.DateField(blank=True, default="2000-01-01")
#     gender = models.CharField(max_length=100, blank=True, default="male")
#     course = models.ForeignKey(Courses, null=True, on_delete=models.SET_NULL)
#     batch = models.ManyToManyField(Batch)
#     isActive = models.BooleanField(default=False)
#     password = models.CharField(max_length=50, default='Nish@@nt111')

#     def __str__(self):
#         return self.Name

# # slots modal


# class Slot(models.Model):
#     duration = models.IntegerField()
#     date = models.DateField(blank=True, default="2000-01-01")
#     time = models.TimeField()


# class DayTimeSlot(models.Model):
#     days_choice = [
#         ('sunday', 'sunday'),
#         ('monday', 'monday'),
#         ('tuesday', 'tuesday'),
#         ('wednesday', 'wednesday'),
#         ('thirsday', 'thirsday'),
#         ('friday', 'friday'),
#         ('saturday', 'saturday'),
#     ]

#     coach = models.ForeignKey(Coach, null=True, on_delete=models.SET_NULL)
#     day = models.CharField(
#         max_length=200, choices=days_choice, default='sunday')
#     start_time_id = models.CharField(
#         blank=True, max_length=200, default="null")
#     end_time_id = models.CharField(blank=True, max_length=2000, default="null")
#     week_id = models.CharField(max_length=200, default="1")
#     isActive = models.BooleanField(default=True)
#     isConfirmed = models.BooleanField(default=False)
#     session_id = models.CharField(max_length=200, default='null')
#     for_learners = models.BooleanField(default=False)


# class LearnerdayTimeSlot(models.Model):
#     learner = models.ForeignKey(Learners, null=True, on_delete=models.SET_NULL)
#     course = models.ForeignKey(Courses, null=True, on_delete=models.SET_NULL)
#     slot = models.ForeignKey(DayTimeSlot, null=True, on_delete=models.SET_NULL)
#     coach = models.ForeignKey(Coach, null=True, on_delete=models.SET_NULL)
#     isActive = models.BooleanField(default=True)
#     isConfirmed = models.BooleanField(default=False)
#     day = models.CharField(max_length=200, default='sunday')


# class CoachCoachySession(models.Model):
#     learner = models.ForeignKey(Learners, null=True, on_delete=models.SET_NULL)
#     batch = models.ForeignKey(Batch, null=True, on_delete=models.SET_NULL)
#     slot = models.OneToOneField(
#         DayTimeSlot, null=True, on_delete=models.SET_NULL)
#     zoomID = models.CharField(max_length=200, default='null')
#     isConfirmedByCoach = models.BooleanField(default=False)
#     isConfirmedByLearner = models.BooleanField(default=False)
#     isActive = models.BooleanField(default=True)
# # sessions api


# class Sessions(models.Model):
#     course = models.ForeignKey(Courses, null=True, on_delete=models.SET_NULL)
#     batch = models.ForeignKey(Batch, null=True, on_delete=models.SET_NULL)
#     sessionNumber = models.IntegerField(blank=True, default="1")
#     start_day = models.DateField(blank=True, default="2000-01-01")
#     end_day = models.DateField(blank=True, default="2000-01-01")


# # import sheet
# class ExcelFileUpload(models.Model):
#     excel_file_upload = models.FileField(upload_to="excel")


# New coach model


class AdminRequest(models.Model):
    assigned_coach = models.ManyToManyField(Coach, related_name='Coach')
    confirmed_coach = models.ManyToManyField(
        Coach, related_name='confirmed_coach', blank=True)
    name = models.CharField(blank=True, max_length=200, default='Request -')
    isActive = models.BooleanField(default=True)
    expire_date = models.DateField(default="2022-09-10")


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
