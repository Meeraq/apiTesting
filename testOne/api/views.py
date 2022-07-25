from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Courses,Learners,Batch,Coach,Faculty,slot
from .serializers import CourseSerializer,LearnerSerializer,BatchSerializer,CoachSerializer,FacultySerializer,SlotSerializer
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
    else:
        return Response(status='500')
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

#faculty api

@api_view(['GET'])

def getfaculty(request):
    coaches = Faculty.objects.all()
    serializer = FacultySerializer(coaches,many=True)
    return Response(serializer.data)


@api_view(['POST'])

def addfaculty(request):
    serializer = FacultySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)



#slot api

@api_view(['GET'])

def getslot(request):
    slots = slot.objects.all()
    serializer = SlotSerializer(slots,many=True)
    return Response(serializer.data)


@api_view(['POST'])

def addslot(request):
    serializer = SlotSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)