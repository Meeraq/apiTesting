from import_export import resources
from .models import ConfirmedSlotsbyCoach


class ConfirmedSlotResource(resources.ModelResource):
    class Meta:
        model = ConfirmedSlotsbyCoach