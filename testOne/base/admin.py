from django.contrib import admin

# Register your models here.
from .models import Batch, Learner, SlotForCoach,AdminRequest,Coach,Profile,ConfirmedSlotsbyCoach,Events,LeanerConfirmedSlots,UserToken,CalendarEvent
from import_export.admin import ImportExportMixin

admin.site.register(Profile)
admin.site.register(SlotForCoach)
admin.site.register(Events)
admin.site.register(LeanerConfirmedSlots)
admin.site.register(Batch)
admin.site.register(Learner)
admin.site.register(Coach)
admin.site.register(AdminRequest)
# admin.site.register(Faculty)
# admin.site.register(Slot)
# admin.site.register(DayTimeSlot)
# admin.site.register(LearnerdayTimeSlot)
# admin.site.register(Sessions)
admin.site.register(UserToken)
admin.site.register(CalendarEvent)



class ExelExport(ImportExportMixin, admin.ModelAdmin):
    list_display = ['start_time', 'end_time', 'date', 'coach_id','SESSION_START_TIME','SESSION_END_TIME','SESSION_DATE']


admin.site.register(ConfirmedSlotsbyCoach,ExelExport)