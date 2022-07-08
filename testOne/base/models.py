from django.db import models



# Learner Modal

class Learners(models.Model):
    learnerName = models.CharField(max_length=200)
    learnerEmail = models.CharField(max_length=100)
    learnerPhoneNumber = models.IntegerField()
    learnerCompany = models.CharField(max_length=100)
    learnerIndustry = models.CharField(max_length=100)
    learnerDesignation = models.CharField(max_length=100)
    learnerDOB = models.CharField(max_length=100)
    learnerGender = models.CharField(max_length=100)
    learnerCourse = models.CharField(max_length=100)
    learnerBatch = models.CharField(max_length=100)

    def __str__(self):
        return self.learnerName

class CourseCategorys(models.Model):
    courseCategoryName = models.CharField(max_length=200)
    def __str__(self):
        return self.courseCategoryName




# Courses Model
class Courses(models.Model):
    courseName = models.CharField(max_length=200)
    courseCategory = models.ForeignKey(CourseCategorys,null=True,on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.courseName

# batch Modal

class Batch(models.Model):
    batchStartDate= models.CharField(max_length=200) 
    batchName = models.CharField(max_length=200)
    batchFaculty = models.CharField(max_length=200)
    batchFees = models.CharField(max_length=200)
    batchFrequency = models.CharField(max_length=200)
    batchNoOfSessions = models.IntegerField()
    course = models.ForeignKey(Courses,null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return self.batchName



# coach Modal

class Coach(models.Model): 
    Name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.IntegerField()
    dob = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    fee = models.IntegerField()
    activeSince = models.CharField(max_length=200)

    def __str__(self):
        return self.Name

