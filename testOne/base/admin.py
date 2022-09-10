from django.contrib import admin

# Register your models here.
from .models import SlotForCoach,AdminRequest,Courses,Learners,Batch,CourseCategorys,Coach,Faculty,Slot,DayTimeSlot,LearnerdayTimeSlot,Sessions,Profile,ConfirmedSlotsbyCoach
from import_export.admin import ImportExportMixin

admin.site.register(Profile)
admin.site.register(SlotForCoach)
admin.site.register(Courses)
admin.site.register(Learners)
admin.site.register(Batch)
admin.site.register(CourseCategorys)
admin.site.register(Coach)
admin.site.register(AdminRequest)
admin.site.register(Faculty)
admin.site.register(Slot)
admin.site.register(DayTimeSlot)
admin.site.register(LearnerdayTimeSlot)
admin.site.register(Sessions)



class ExelExport(ImportExportMixin, admin.ModelAdmin):
    list_display = ['start_time', 'end_time', 'date', 'coach_id','SESSION_START_TIME','SESSION_END_TIME','SESSION_DATE']


admin.site.register(ConfirmedSlotsbyCoach,ExelExport)