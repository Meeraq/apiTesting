from dataclasses import field
from rest_framework import serializers
from base.models import Coach, Profile
from django.contrib.auth.models import User


from base.models import SlotForCoach
from base.models import ConfirmedSlotsbyCoach
from base.models import AdminRequest
from base.models import Events, LeanerConfirmedSlots
from base.models import DeleteConfirmedSlotsbyAdmin
from base.models import Learner
from base.models import Batch


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'is_staff']

class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username']

class ProfileSerializer(serializers.ModelSerializer):
    userDetails = UserSerializer(required=False)

    class Meta:
        model = Profile
        fields = '__all__'



class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'email', 'phone', 'dob', 'gender', 'fee',
                  'activeSince', 'isSlotBooked', 'isActive', 'meet_link']


class SlotForCoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlotForCoach
        fields = '__all__'


class ConfirmedSlotsbyCoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmedSlotsbyCoach
        fields = '__all__'


class AdminReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminRequest
        fields = ['isActive', 'expire_date', 'name']


class GetAdminReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminRequest
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'

class ConfirmedSlotsbyLearnerSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = LeanerConfirmedSlots
        fields = '__all__'

class ConfirmedLearnerSerializer(serializers.ModelSerializer):
    slot = ConfirmedSlotsbyCoachSerializer()
    class Meta:
        model = LeanerConfirmedSlots
        fields = '__all__'

class dltSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeleteConfirmedSlotsbyAdmin
        fields = '__all__'


class LearnerDataUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Learner
        fields = '__all__'

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'


