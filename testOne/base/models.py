from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Profile(models.Model):
    user_choice = [
        ('coach','coach'),
        ('admin','admin'),
        ('learner','learner'),
        ('faculty','faculty')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50,choices=user_choice,default='coach')
    email = models.CharField(max_length=200,default="a@gmail.com")

    def __str__(self):
        return self.user.username






class CourseCategorys(models.Model):
    courseCategoryName = models.CharField(max_length=200)
    def __str__(self):
        return self.courseCategoryName




# Courses Model
class Courses(models.Model):
    Name = models.CharField(max_length=200)
    category = models.ForeignKey(CourseCategorys,null=True,on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    course_id = models.CharField(max_length=200,default='0000')
    isActive = models.BooleanField(default=False)

    def __str__(self):
        return self.Name

# batch Modal

class Batch(models.Model):
    StartDate= models.DateField(blank=True,default="2000-01-01")
    Name = models.CharField(max_length=200)
    Faculty = models.CharField(max_length=200)
    Fees = models.CharField(max_length=200)
    Frequency = models.CharField(max_length=200)
    NoOfSessions = models.IntegerField()
    course = models.ForeignKey(Courses,null=True,on_delete=models.SET_NULL)
    isActive = models.BooleanField(default=False)
    duration = models.IntegerField(default=30)

    def __str__(self):
        return self.Name



# coach Modal

class Coach(models.Model): 
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=2000)
    dob = models.DateField(blank=True,default="2000-01-01")
    gender = models.CharField(max_length=200,blank=True)
    fee = models.IntegerField(blank=True,default="6000")
    activeSince = models.DateField(blank=True,default="2000-01-01")
    isSlotBooked = models.BooleanField(default=False,blank=True)
    isActive = models.BooleanField(default=False,blank=True)
    password = models.CharField(max_length=50,default='Nish@@nt111')

    def __str__(self):
        return self.name



# Faculty Modal

class Faculty(models.Model): 
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=2000)
    dob = models.DateField(blank=True,default="2000-01-01")
    gender = models.CharField(max_length=200,blank=True)
    fee = models.IntegerField(blank=True,default="6000")
    activeSince = models.DateField(blank=True,default="2000-01-01")
    isActive = models.BooleanField(default=False,blank=True)
    password = models.CharField(max_length=50,default='Nish@@nt111')

    def __str__(self):
        return self.name


# Learner Modal

class Learners(models.Model):
    Name = models.CharField(max_length=200)
    Email = models.CharField(max_length=100)
    PhoneNumber = models.CharField(max_length=1000,default="7880647282")
    Company = models.CharField(max_length=100,blank=True,default="000")
    Industry = models.CharField(max_length=100,blank=True,default="000")
    Designation = models.CharField(max_length=100,blank=True,default="000")
    DOB = models.DateField(blank=True,default="2000-01-01")
    Gender = models.CharField(max_length=100,blank=True,default="male")
    Course = models.ForeignKey(Courses,null=True,on_delete=models.SET_NULL)
    Batch = models.ManyToManyField(Batch)
    isActive = models.BooleanField(default=False)
    password = models.CharField(max_length=50,default='Nish@@nt111')

    def __str__(self):
        return self.Name

# slots modal 


class Slot(models.Model): 
    duration = models.IntegerField()
    date = models.DateField(blank=True,default="2000-01-01")
    time = models.TimeField()



class DayTimeSlot(models.Model): 
    days_choice = [
        ('sunday','sunday'),
        ('monday','monday'),
        ('tuesday','tuesday'),
        ('wednesday','wednesday'),
        ('thirsday','thirsday'),
        ('friday','friday'),
        ('saturday','saturday'),
    ]

    coach = models.ForeignKey(Coach,null=True,on_delete=models.SET_NULL)
    day = models.CharField(max_length=2000,choices=days_choice,default='sunday')
    start_time_id = models.DateField(blank=True,default="2000-01-01")
    end_time_id = models.DateField(blank=True,default="2000-01-01")
    week_id = models.CharField(max_length=200,default="1")
    isActive = models.BooleanField(default=True)
    isConfirmed = models.BooleanField(default=False)
    session_id = models.CharField(max_length=200,default='null')
    


class LearnerdayTimeSlot(models.Model): 
    learner = models.ForeignKey(Learners,null=True,on_delete=models.SET_NULL)
    course = models.ForeignKey(Courses,null=True,on_delete=models.SET_NULL)
    slot = models.ForeignKey(DayTimeSlot,null=True,on_delete=models.SET_NULL)
    coach = models.ForeignKey(Coach,null=True,on_delete=models.SET_NULL)
    isActive = models.BooleanField(default=True)
    isConfirmed = models.BooleanField(default=False)
    day = models.CharField(max_length=200,default='sunday')
    

# sessions api 


class Sessions(models.Model): 
    course = models.ForeignKey(Courses,null=True,on_delete=models.SET_NULL)
    batch = models.ForeignKey(Batch,null=True,on_delete=models.SET_NULL)
    sessionNumber = models.IntegerField(blank=True,default="1")
    start_day = models.DateField(blank=True,default="2000-01-01")
    end_day = models.DateField(blank=True,default="2000-01-01")
    

# # import sheet 
# class ExcelFileUpload(models.Model):
#     excel_file_upload = models.FileField(upload_to="excel")