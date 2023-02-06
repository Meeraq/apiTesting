from django.contrib import admin

# Register your models here.
from .models import Batch, CoachPrice, Learner, SlotForCoach, AdminRequest, Coach, Profile, ConfirmedSlotsbyCoach, Events, LeanerConfirmedSlots, DeleteConfirmedSlotsbyAdmin, ServiceApproval, PurchaseOrder, StatusUpdateRequest  # ServiceApprovalData #ServiceApprovalEntry
from import_export.admin import ImportExportMixin

admin.site.register(Profile)
admin.site.register(SlotForCoach)
admin.site.register(Events)
admin.site.register(LeanerConfirmedSlots)
admin.site.register(Batch)
admin.site.register(Learner)
admin.site.register(Coach)
admin.site.register(AdminRequest)
# admin.site.register(ServiceApprovalData)
admin.site.register(DeleteConfirmedSlotsbyAdmin)
admin.site.register(CoachPrice)
admin.site.register(ServiceApproval)
admin.site.register(PurchaseOrder)
admin.site.register(StatusUpdateRequest)


class ExelExport(ImportExportMixin, admin.ModelAdmin):
    list_display = ['start_time', 'end_time', 'date', 'coach_id',
                    'SESSION_START_TIME', 'SESSION_END_TIME', 'SESSION_DATE']


admin.site.register(ConfirmedSlotsbyCoach, ExelExport)
