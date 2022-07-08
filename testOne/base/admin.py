from django.contrib import admin

# Register your models here.
from .models import Courses,Learners,Batch,CourseCategorys,Coach

admin.site.register(Courses)
admin.site.register(Learners)
admin.site.register(Batch)
admin.site.register(CourseCategorys)
admin.site.register(Coach)