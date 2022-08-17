from django.forms import ValidationError
from rest_framework.response import Response
from django.http import JsonResponse
# import pandas as pd
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from base.models import Courses,Learners,Batch,Coach,Faculty,Slot,DayTimeSlot,LearnerdayTimeSlot,Sessions,Profile
# from base.models import ExcelFileUpload
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .serializers import CourseSerializer,LearnerSerializer,BatchSerializer,CoachSerializer,FacultySerializer,SlotSerializer,SlotTimeDaySerializer,LearnerSlotTimeDaySerializer,SessionSerializer,UserSerializer,ProfileSerializer
import json




# courses api functions

@api_view(['GET'])
@permission_classes([AllowAny])
def getCourses(request):
    courses = Courses.objects.all()
    serializer = CourseSerializer(courses,many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def addCourses(request):
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response({'status':'400 Bad request','Reason':'Wrong data sent'})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateCourses(request,_id):
    course = Courses.objects.get(id=_id)
    serializer = CourseSerializer(instance=course,data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response({'status':'400 Bad request','Reason':'Wrong data sent'})
    return Response(serializer.data)


# Learner Api Functions

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getLearners(request):
    learners = Learners.objects.all()
    serializer = LearnerSerializer(learners,many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def addLearners(request):
    serializer = LearnerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateLearners(request,_id):
    learner = Learners.objects.get(id=_id)
    serializer = LearnerSerializer(instance=learner,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

#batch api

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBatches(request):
    batches = Batch.objects.all()
    serializer = BatchSerializer(batches,many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addBatches(request):
    serializer = BatchSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateBatches(request,_id):
    batch = Batch.objects.get(id=_id)
    serializer = BatchSerializer(instance=batch,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


#coach api

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getcoach(request):
    coaches = Coach.objects.all()
    serializer = CoachSerializer(coaches,many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([AllowAny])
def addcoach(request):
    coachSerializer = CoachSerializer(data=request.data)
    if coachSerializer.is_valid():
        newUser = User(username=coachSerializer.data['name'],email=coachSerializer.data['email'],password = coachSerializer.data['password'])
        newUser.save()
        userToSave = User.objects.get(email=coachSerializer.data['email'])
        newProfile = Profile(user=userToSave,type="coach",email=coachSerializer.data['email'])
        newProfile.save()
        coachSerializer.userProfile = newProfile
        coachSerializer.save()
    else:
        print(coachSerializer.errors)
        return Response(status='403')
    for user in User.objects.all():
        token = Token.objects.get_or_create(user=user)
    return Response({'status': 200,'payload':coachSerializer.data,'token':str(token[0])})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateCoach(request,_id):
    coach = Coach.objects.get(id=_id)
    serializer = CoachSerializer(instance=coach,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

#faculty api

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getfaculty(request):
    coaches = Faculty.objects.all()
    serializer = FacultySerializer(coaches,many=True)
    return Response(serializer.data)



@api_view(['POST'])

def addfaculty(request):
    serializer = FacultySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        newUser = User(username=serializer.data['name'],password = serializer.data['password'])
        newUser.save()
    else:
        print(serializer.errors)
        return Response(status='403')
    for user in User.objects.all():
        token = Token.objects.get_or_create(user=user)
    return Response({'status': 200,'payload':serializer.data,'token':str(token)})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateFaculty(request,_id):
    faculty = Faculty.objects.get(id=_id)
    serializer = FacultySerializer(instance=faculty,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

#slot api

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getslot(request):
    slots = Slot.objects.all()
    serializer = SlotSerializer(slots,many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addslot(request):
    serializer = SlotSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getDayTimeslot(request):
    slots = DayTimeSlot.objects.all()
    serializer = SlotTimeDaySerializer(slots,many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addDayTimeslot(request):
    for day in request.data:
            newdayTimeSlot =  DayTimeSlot(coach=day['coach'],dayofmock = day['dayofmock'],start_time_id = day['start_time_id'], end_time_id = day['end_time_id'])
            newdayTimeSlot.save()

    slots = DayTimeSlot.objects.all()
    serializer = SlotTimeDaySerializer(slots,many=True)
    return Response({'status':200,'data':serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateDayTimeslot(request,_id):
    slot = DayTimeSlot.objects.get(id=_id)
    serializer = SlotTimeDaySerializer(instance=slot,data=request.data)
    if serializer.is_valid():
        serializer.save()

    slots = DayTimeSlot.objects.all()
    serializer = SlotTimeDaySerializer(slots,many=True)
    return Response({'status': 200,'data':serializer.data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteDayTimeslot(request,_id):
    slot = DayTimeSlot.objects.get(id=_id)
    slot.delete()

    slots = DayTimeSlot.objects.all()
    serializer = SlotTimeDaySerializer(slots,many=True)
    return Response({'status': 200,'data':serializer.data})

#learner slot book


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def learnergetDayTimeslot(request):
    slots = LearnerdayTimeSlot.objects.all()
    serializer = LearnerSlotTimeDaySerializer(slots,many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addLearnerDayTimeslot(request):
    for day in request.data:
            newdayTimeSlot =  LearnerdayTimeSlot(learner=day['learner'],start_time_id = day['start_time_id'], end_time_id = day['end_time_id'])
            newdayTimeSlot.save()
    slots = LearnerdayTimeSlot.objects.all()
    serializer = LearnerSlotTimeDaySerializer(slots,many=True)
    return Response({'status':200,'data':serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateLearnerDayTimeslot(request,_id):
    slot = LearnerdayTimeSlot.objects.get(id=_id)
    serializer = LearnerSlotTimeDaySerializer(instance=slot,data=request.data)
    if serializer.is_valid():
        serializer.save()

    slots = LearnerdayTimeSlot.objects.all()
    serializer = LearnerSlotTimeDaySerializer(slots,many=True)
    return Response({'status': 200,'data':serializer.data})




# sessions 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSessions(request):
    session = Sessions.objects.all()
    serializer = SessionSerializer(session,many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addSession(request):
    serializer = SessionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response({'status':'400 Bad request','Reason':'Wrong data sent'})
    return Response(serializer.data)




# log in


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    userName = request.data['username']
    email = request.data['email']
    password = request.data['password']
    
    try:
        account = User.objects.get(username = userName)
        userProfile = account.profile
        if userProfile.type == 'coach':
            userProfileDetails = userProfile.coach
        elif userType.type == 'learner':
            userProfileDetails = userProfile.learner
        elif userType.type == 'faculty':
            userProfileDetails = userProfile.faculty
    except BaseException as e:
        raise ValidationError({"400":f'{str(e)}'})
    if password == account.password:
        token = Token.objects.get_or_create(user = account)
    else:
        raise ValidationError({"message": "Incorrect Login credentials"})
    return JsonResponse({'status':'200','username':account.username,'token':str(token[0]),'email':userProfile.email,'usertype':userType.type,"id":userProfile.id})







@api_view(['POST'])
@permission_classes([AllowAny])
def registerUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(status='403')
    user = User.objects.get(username = serializer.data['username'])
    token , _ = Token.objects.get_or_create(user=user)
    return Response({'status': 200,'payload':serializer.data,'token':str(token)})




@api_view(['POST'])
@permission_classes([AllowAny])
def addProfileType(request):
    serializer = ProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response({'status':'400 Bad request','Reason':'Wrong data sent'})
    return Response(serializer.data)