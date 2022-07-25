from django.db import models



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

    def __str__(self):
        return self.Name

class CourseCategorys(models.Model):
    courseCategoryName = models.CharField(max_length=200)
    def __str__(self):
        return self.courseCategoryName




# Courses Model
class Courses(models.Model):
    Name = models.CharField(max_length=200)
    Category = models.ForeignKey(CourseCategorys,null=True,on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

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

    def __str__(self):
        return self.name


# slots modal 


class slot(models.Model): 
    duration = models.IntegerField()
    date = models.DateField(blank=True,default="2000-01-01")
    time = models.TimeField()
