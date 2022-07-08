from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Courses,Learners,Batch,Coach
from .serializers import CourseSerializer,LearnerSerializer,BatchSerializer,CoachSerializer
# courses api functions

@api_view(['GET'])

def getCourses(request):
    courses = Courses.objects.all()
    serializer = CourseSerializer(courses,many=True)
    return Response(serializer.data)


@api_view(['POST'])

def addCourses(request):
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)



# Learner Api Functions

@api_view(['GET'])

def getLearners(request):
    learners = Learners.objects.all()
    serializer = LearnerSerializer(learners,many=True)
    return Response(serializer.data)


@api_view(['POST'])

def addLearners(request):
    serializer = LearnerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)



#batch api

@api_view(['POST'])

def addBatches(request):
    serializer = BatchSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)



#coach api

@api_view(['GET'])

def getcoach(request):
    coaches = Coach.objects.all()
    serializer = CoachSerializer(coaches,many=True)
    return Response(serializer.data)


@api_view(['POST'])

def addcoach(request):
    serializer = CoachSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
