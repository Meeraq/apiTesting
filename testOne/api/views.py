from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Courses,Learners
from .serializers import CourseSerializer,LearnerSerializer

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

