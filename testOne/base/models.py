from django.db import models
from django.contrib.auth.models import User




class customUser(User):
    def _init__(self,type):
        self.type = type
    type = models.CharField(max_length=100)
    

# Learner Modal

class Learners(models.Model):
    Name = models.CharField(max_length=200)
    Email = models.CharField(max_length=100)
    PhoneNumber = models.CharField(max_length=1000,default="7880647282")
    Company = models.CharField(max_length=100)
    Industry = models.CharField(max_length=100)
    Designation = models.CharField(max_length=100)
    DOB = models.DateField(blank=True,default="2000-01-01")
    Gender = models.CharField(max_length=100)
    Course = models.CharField(max_length=100)
    Batch = models.CharField(max_length=100)
    isActive = models.BooleanField(default=False)
    password = models.CharField(max_length=50,default='Nish@@nt111')

    def __str__(self):
        return self.Name

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
    gender = models.CharField(max_length=200)
    fee = models.IntegerField()
    activeSince = models.DateField(blank=True,default="2000-01-01")
    isSlotBooked = models.BooleanField(default=False)
    isActive = models.BooleanField(default=False)
    password = models.CharField(max_length=50,default='Nish@@nt111')

    def __str__(self):
        return self.name



# Faculty Modal

class Faculty(models.Model): 
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=2000)
    dob = models.DateField(blank=True,default="2000-01-01")
    gender = models.CharField(max_length=200)
    fee = models.IntegerField()
    activeSince = models.DateField(blank=True,default="2000-01-01")
    isActive = models.BooleanField(default=False)
    password = models.CharField(max_length=50,default='Nish@@nt111')

    def __str__(self):
        return self.name


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

    # coach = models.ForeignKey(Coach,null=True,on_delete=models.SET_NULL)
    coach = models.CharField(max_length=200,default='nishant')
    dayofmock = models.CharField(max_length=2000,choices=days_choice,default='sunday')
    start_time_id = models.CharField(max_length=200)
    end_time_id = models.CharField(max_length=200)
    


class LearnerdayTimeSlot(models.Model): 
    learner = models.CharField(max_length=200,default='nishant')
    start_time_id = models.CharField(max_length=200)
    end_time_id = models.CharField(max_length=200)
    

# sessions api 

class Sessions(models.Model): 
    course = models.ForeignKey(Courses,null=True,on_delete=models.SET_NULL)
    weekStart= models.CharField(max_length=200,default='Null')
    weekEnd= models.CharField(max_length=200,default='Null')
    dayOne= models.CharField(max_length=200,default='Null')
    dayTwo = models.CharField(max_length=200,default='Null')
    dayThree = models.CharField(max_length=200,default='Null')
    dayFour = models.CharField(max_length=200,default='Null')

# import sheet 
class ExcelFileUpload(models.Model):
    excel_file_upload = models.FileField(upload_to="excel")