from django.db import models

# Courses Model
class Courses(models.Model):
    courseName = models.CharField(max_length=200)
    courseCategory = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)


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