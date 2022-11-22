from import_export import resources, fields
from .models import ConfirmedSlotsbyCoach, LeanerConfirmedSlots


class ConfirmedSlotResource(resources.ModelResource):
    class Meta:
        model = ConfirmedSlotsbyCoach
        exclude = ('date', 'start_time', 'end_time', 'coach_id')


class LearnerConfirmedSlotsResource(resources.ModelResource):
    slot__COACH_NAME = fields.Field(
        attribute="slot__COACH_NAME", column_name="Coach")
    name = fields.Field(attribute="name", column_name="Learner's Name")
    email = fields.Field(attribute="email", column_name="Learner's Email")
    phone_no = fields.Field(attribute="phone_no",
                            column_name="Learner's Phone")
    slot__SESSION_START_TIME = fields.Field(
        attribute="slot__SESSION_START_TIME", column_name="Session Time")
    slot__date = fields.Field(
        attribute="slot__date", column_name="Session Date")

    class Meta:
        model = LeanerConfirmedSlots
        fields = ('slot__COACH_NAME', 'name', 'email', 'phone_no',
                  'organization', 'slot__date', 'slot__SESSION_START_TIME')
