from dataclasses import field
from rest_framework import serializers
from base.models import Courses,Learners,Batch,Coach,Faculty,Slot,DayTimeSlot,LearnerdayTimeSlot,Sessions,Profile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password','is_staff']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
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
        fields = '__all__'

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'


class SlotTimeDaySerializer(serializers.ModelSerializer):
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