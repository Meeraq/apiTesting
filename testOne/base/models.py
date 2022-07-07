from django.db import models


def __str__(self):
    return self.learnerName
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



# batch Modal

class Batch(models.Model):
    batchStartDate= models.CharField(max_length=200)
    batchName = models.CharField(max_length=200)
    batchFaculty = models.CharField(max_length=200)
    batchFees = models.CharField(max_length=200)
    batchFrequency = models.CharField(max_length=200)
    batchNoOfSessions = models.IntegerField()


def __str__(self):
    return self.courseName

# Courses Model
class Courses(models.Model):
    courseName = models.CharField(max_length=200)
    courseCategory = models.CharField(max_length=200)
    batch = models.ForeignKey(Batch,null=True,on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)