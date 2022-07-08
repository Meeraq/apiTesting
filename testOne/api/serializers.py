from dataclasses import field
from rest_framework import serializers
from base.models import Courses,Learners,Batch,Coach

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


class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = '__all__'
