from dataclasses import field
from rest_framework import serializers
from base.models import Coach, Profile
from django.contrib.auth.models import User


from base.models import SlotForCoach
from base.models import ConfirmedSlotsbyCoach
from base.models import AdminRequest
from base.models import Events, LeanerConfirmedSlots


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


# class CourseCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CourseCategorys
#         fields = '__all__'


# class CourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Courses
#         fields = '__all__'


# class LearnerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Learners
#         fields = ['id', 'name', 'email', 'phone', 'company', 'industry', 'designation', 'dob', 'gender',
#                   'course', 'batch', 'isActive']


# class BatchSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Batch
#         fields = '__all__'

# # class Coach():


class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'email', 'phone', 'dob', 'gender', 'fee',
                  'activeSince', 'isSlotBooked', 'isActive', 'meet_link']


# class FacultySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Faculty
#         fields = ['id', 'name', 'email', 'phone', 'dob', 'gender', 'fee',
#                   'activeSince', 'isActive']


# class SlotSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Slot
#         fields = '__all__'


# class CoachCoachySessionSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = CoachCoachySession
#         fields = '__all__'


# class SlotTimeDaySerializer(serializers.ModelSerializer):
#     coachcoachysession = CoachCoachySessionSerializer(required=False)

#     class Meta:
#         model = DayTimeSlot
#         fields = '__all__'


# class LearnerSlotTimeDaySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LearnerdayTimeSlot
#         fields = '__all__'


# class SessionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Sessions
#         fields = '__all__'


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