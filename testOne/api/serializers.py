from dataclasses import field
from rest_framework import serializers
from base.models import Courses,Learners,Batch,Coach,Faculty,Slot,DayTimeSlot,LearnerdayTimeSlot,Sessions,Profile,CourseCategorys
from django.contrib.auth.models import User

from base.models import CoachCoachySession


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password','is_staff']


class ProfileSerializer(serializers.ModelSerializer):
    userDetails = UserSerializer(required=False)
    class Meta:
        model = Profile
        fields = '__all__'

class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategorys
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'

class LearnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Learners
        fields = '__all__'


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'

# class Coach():

class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = ['name','email','phone','dob','gender','fee','activeSince','isSlotBooked','isActive','password']

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'


class CoachCoachySessionSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = CoachCoachySession
        fields = '__all__'

class SlotTimeDaySerializer(serializers.ModelSerializer):
    coachcoachysession = CoachCoachySessionSerializer(required=False)
    class Meta:
        model = DayTimeSlot
        fields = '__all__'

class LearnerSlotTimeDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnerdayTimeSlot
        fields = '__all__'


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sessions
        fields = '__all__'