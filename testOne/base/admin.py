from django.contrib import admin

# Register your models here.
from .models import Courses,Learners,Batch,CourseCategorys,Coach,Faculty,Slot,DayTimeSlot,LearnerdayTimeSlot,Sessions,Profile
# SessionOneStartEnd,SessionTwoStartEnd

admin.site.register(Profile)
admin.site.register(Courses)
admin.site.register(Learners)
admin.site.register(Batch)
admin.site.register(CourseCategorys)
admin.site.register(Coach)
admin.site.register(Faculty)
admin.site.register(Slot)
admin.site.register(DayTimeSlot)
admin.site.register(LearnerdayTimeSlot)
admin.site.register(Sessions)
# admin.site.register(SessionOneStartEnd)
# admin.site.register(SessionTwoStartEnd)