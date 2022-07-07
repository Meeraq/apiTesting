from django.contrib import admin

# Register your models here.
from .models import Courses,Learners,Batch

admin.site.register(Courses)
admin.site.register(Learners)
admin.site.register(Batch)