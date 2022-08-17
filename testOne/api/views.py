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
    serializer = CoachSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        newUser = User(username=serializer.data['name'],email=serializer.data['email'],password = serializer.data['password'])
        newUser.save()
        userToSave = User.objects.get(email=serializer.data['email'])
        newProfile = Profile(user=userToSave,type="coach",email=serializer.data['email'])
        newProfile.save()
    else:
        print(serializer.errors)
        return Response(status='403')
    for user in User.objects.all():
        token = Token.objects.get_or_create(user=user)
    return Response({'status': 200,'payload':serializer.data,'token':str(token[0])})


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
        userToSave = User.objects.get(email=serializer.data['email'])
        newProfile = Profile(user=userToSave,type="faculty",email=serializer.data['email'])
        newProfile.save()
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
    for eachDay in request.data:
            coachToSave = Coach.objects.get(id=eachDay['coach'])
            newdayTimeSlot =  DayTimeSlot(
                    coach=coachToSave,
                    day = eachDay['day'],
                    start_time_id = eachDay['start_time_id'],
                    end_time_id = eachDay['end_time_id'],
										week_id = eachDay['week_id']
                    )
            newdayTimeSlot.save()

    slots = DayTimeSlot.objects.filter(coach=coachToSave) ## only return the slots for the specific coach
    serializer = SlotTimeDaySerializer(slots,many=True)
    return Response({'status':200,'data':serializer.data})

# confirm day time slot
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirmDayTimeSlot(request):
    for eachDay in request.data:
            coachToSave = Coach.objects.get(id=eachDay['coach'])
            newdayTimeSlot =  DayTimeSlot(
                    coach=coachToSave,
                    day = eachDay['day'],
                    start_time_id = eachDay['start_time_id'],
                    end_time_id = eachDay['end_time_id'],
										week_id = eachDay['week_id'],
										isConfirmed = True
                    )
            newdayTimeSlot.save()
    slots = DayTimeSlot.objects.filter(coach=coachToSave,isConfirmed = True) ## only return the confirmed slots for the specific coach 
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
    for session in request.data:
        print(session)
        courseToSave = Courses.objects.get(id=session['course'])
        batchToSave = Batch.objects.get(id=session['batch'])
        newSession = Sessions(course=courseToSave ,batch=batchToSave ,sessionNumber=session['sessionNumber'],start_day=session['start_day'],end_day=session['end_day'])
        newSession.save()
    sessions = Sessions.objects.all()
    serializer = SessionSerializer(sessions,many=True)
    return Response({'status':200,'data':serializer.data})




# log in


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    userName = request.data['username']
    email = request.data['email']
    password = request.data['password']
    
    try:
        Account = User.objects.get(username = userName)
        userType = Profile.objects.get(email = email)
        if userType.type == 'coach':
            userProfile = Coach.objects.get(email = email)
        elif userType.type == 'learner':
            userProfile = Learners.objects.get(email = email)
        elif userType.type == 'faculty':
            userProfile = Faculty.objects.get(email = email)
    except BaseException as e:
        raise ValidationError({"400":f'{str(e)}'})
    if password == Account.password:
        token = Token.objects.get_or_create(user = Account)
    else:
        raise ValidationError({"message": "Incorrect Login credentials"})
    return Response({'status':'200','username':Account.username,'token':str(token[0]),'email':userProfile.email,'usertype':userType.type,"id":userProfile.id})







@api_view(['POST'])
@permission_classes([AllowAny])
def registerUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(status='403')
    user = User.objects.get(username = serializer.data['username'])
    userToSave = User.objects.get(email=serializer.data['email'])
    newProfile = Profile(user=userToSave,type="admin",email=serializer.data['email'])
    newProfile.save()
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