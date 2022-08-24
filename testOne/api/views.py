from urllib import response
from django.forms import ValidationError
from rest_framework.response import Response
from django.http import JsonResponse
# import pandas as pd
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from base.models import Courses, Learners, Batch, Coach, Faculty, Slot, DayTimeSlot, LearnerdayTimeSlot, Sessions, Profile, CoachCoachySession, CourseCategorys
# from base.models import ExcelFileUpload
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import CoachCoachySessionSerializer, CourseSerializer, LearnerSerializer, BatchSerializer, CoachSerializer, FacultySerializer, SlotSerializer, SlotTimeDaySerializer, LearnerSlotTimeDaySerializer, SessionSerializer, UserSerializer, ProfileSerializer, CourseCategorySerializer
from django.db.models import Q


# sesame
from sesame.utils import get_query_string, get_user
# from sesame.utils import get_query_string, get_user


# courses api functions

@api_view(['GET'])
@permission_classes([AllowAny])
def getCourses(request):
    courses = Courses.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def addCourses(request):
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response({'status': '400 Bad request', 'Reason': 'Wrong data sent'})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateCourses(request, _id):
    course = Courses.objects.get(id=_id)
    serializer = CourseSerializer(instance=course, data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response({'status': '400 Bad request', 'Reason': 'Wrong data sent'})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def getCourseCategory(request):
    category = CourseCategorys.objects.all()
    serializer = CourseCategorySerializer(category, many=True)
    return Response(serializer.data)

# Learner Api Functions


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getLearners(request):
    learners = Learners.objects.all()
    serializer = LearnerSerializer(learners, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def addLearners(request):
    serializer = LearnerSerializer(data=request.data)
    if serializer.is_valid():
        newUser = User.objects.create_user(
            username=request.data['email'], password='Meeraq@123')
        newUser.save()
        userToSave = User.objects.get(username=request.data['email'])
        newProfile = Profile(user=userToSave, type="learner",
                             email=request.data['email'])
        newProfile.save()
        serializer.save(user_id=newProfile.id)
    for user in User.objects.all():
        Token.objects.get_or_create(user=user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateLearners(request, _id):
    learner = Learners.objects.get(id=_id)
    serializer = LearnerSerializer(instance=learner, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

# batch api


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBatches(request):
    batches = Batch.objects.all()
    serializer = BatchSerializer(batches, many=True)
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
def updateBatches(request, _id):
    batch = Batch.objects.get(id=_id)
    serializer = BatchSerializer(instance=batch, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


# coach api

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getcoach(request):
    coaches = Coach.objects.all()
    serializer = CoachSerializer(coaches, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def addcoach(request):
    serializer = CoachSerializer(data=request.data)
    if serializer.is_valid():
        newUser = User.objects.create_user(
            username=request.data['email'], email=request.data['email'], password=request.data['password'])
        newUser.save()
        userToSave = User.objects.get(username=request.data['email'])
        newProfile = Profile(user=userToSave, type="coach",
                             email=request.data['email'])
        newProfile.save()
        serializer.save(user_id=newProfile.id)

        for user in User.objects.all():
            token = Token.objects.get_or_create(user=user)
    else:
        print(serializer.errors)
        return Response(status='403')
    return Response({'status': 200, 'payload': serializer.data, 'token': str(token[0])})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateCoach(request, _id):
    coach = Coach.objects.get(id=_id)
    serializer = CoachSerializer(instance=coach, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

# faculty api


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getfaculty(request):
    coaches = Faculty.objects.all()
    serializer = FacultySerializer(coaches, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def addfaculty(request):
    serializer = FacultySerializer(data=request.data)
    if serializer.is_valid():
        newUser = User.objects.create_user(
            username=request.data['email'], password='Meeraq@123')
        newUser.save()
        userToSave = User.objects.get(username=request.data['email'])
        newProfile = Profile(user=userToSave, type="faculty",
                             email=request.data['email'])
        newProfile.save()
        serializer.save(user_id=newProfile.id)
    else:
        print(serializer.errors)
        return Response(status='403')
    for user in User.objects.all():
        token = Token.objects.get_or_create(user=user)
    return Response({'status': 200, 'payload': serializer.data, 'token': str(token[0])})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateFaculty(request, _id):
    faculty = Faculty.objects.get(id=_id)
    serializer = FacultySerializer(instance=faculty, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

# slot api


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getslot(request):
    slots = Slot.objects.all()
    serializer = SlotSerializer(slots, many=True)
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
    serializer = SlotTimeDaySerializer(slots, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addDayTimeslot(request):
    for eachDay in request.data:
        coachToSave = Coach.objects.get(id=eachDay['coach'])
        newdayTimeSlot = DayTimeSlot(
            coach=coachToSave,
            day=eachDay['day'],
            start_time_id=eachDay['start_time_id'],
            end_time_id=eachDay['end_time_id'],
            week_id=eachDay['week_id']
        )
        newdayTimeSlot.save()

    # only return the slots for the specific coach
    slots = DayTimeSlot.objects.filter(coach=coachToSave)
    serializer = SlotTimeDaySerializer(slots, many=True)
    return Response({'status': 200, 'data': serializer.data})

# confirm day time slot


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirmDayTimeSlot(request):
    for eachDay in request.data:
        coachToSave = Coach.objects.get(id=eachDay['coach'])
        newdayTimeSlot = DayTimeSlot(
            coach=coachToSave,
            day=eachDay['day'],
            start_time_id=eachDay['start_time_id'],
            end_time_id=eachDay['end_time_id'],
            week_id=eachDay['week_id'],
            isConfirmed=True
        )
        newdayTimeSlot.save()
        currTime = int(eachDay['start_time_id'])
        endTime = int(eachDay['end_time_id'])
        while currTime + 1800000 <= endTime:
            learnerSlot = DayTimeSlot(
                coach=coachToSave,
                day=eachDay['day'],
                start_time_id=str(currTime),
                end_time_id=str(currTime + 1800000),
                week_id=eachDay['week_id'],
                isConfirmed=True,
                for_learners=True
            )
            currTime += 2700000
            learnerSlot.save()
    # only return the confirmed slots for the specific coach
    slots = DayTimeSlot.objects.filter(
        coach=coachToSave, isConfirmed=True, for_learners=False)
    serializer = SlotTimeDaySerializer(slots, many=True)
    return Response({'status': 200, 'data': serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateDayTimeslot(request, _id):
    slot = DayTimeSlot.objects.get(id=_id)
    serializer = SlotTimeDaySerializer(instance=slot, data=request.data)
    if serializer.is_valid():
        serializer.save()

    slots = DayTimeSlot.objects.all()
    serializer = SlotTimeDaySerializer(slots, many=True)
    return Response({'status': 200, 'data': serializer.data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteDayTimeslot(request, _id):
    slot = DayTimeSlot.objects.get(id=_id)
    slot.delete()

    slots = DayTimeSlot.objects.all()
    serializer = SlotTimeDaySerializer(slots, many=True)
    return Response({'status': 200, 'data': serializer.data})

# learner slot book


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def learnergetDayTimeslot(request):
    slots = LearnerdayTimeSlot.objects.all()
    serializer = LearnerSlotTimeDaySerializer(slots, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addLearnerDayTimeslot(request):
    for day in request.data:
        newdayTimeSlot = LearnerdayTimeSlot(
            learner=day['learner'], start_time_id=day['start_time_id'], end_time_id=day['end_time_id'])
        newdayTimeSlot.save()
    slots = LearnerdayTimeSlot.objects.all()
    serializer = LearnerSlotTimeDaySerializer(slots, many=True)
    return Response({'status': 200, 'data': serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateLearnerDayTimeslot(request, _id):
    slot = LearnerdayTimeSlot.objects.get(id=_id)
    serializer = LearnerSlotTimeDaySerializer(instance=slot, data=request.data)
    if serializer.is_valid():
        serializer.save()

    slots = LearnerdayTimeSlot.objects.all()
    serializer = LearnerSlotTimeDaySerializer(slots, many=True)
    return Response({'status': 200, 'data': serializer.data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def LearnerdeleteDayTimeslot(request, _id):
    slot = LearnerdayTimeSlot.objects.get(id=_id)
    slot.delete()
    slots = LearnerdayTimeSlot.objects.all()
    serializer = LearnerSlotTimeDaySerializer(slots, many=True)
    return Response({'status': 200, 'data': serializer.data})


# sessions

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSessions(request):
    session = Sessions.objects.all()
    serializer = SessionSerializer(session, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addSession(request):
    for session in request.data:
        print(session)
        courseToSave = Courses.objects.get(id=session['course'])
        batchToSave = Batch.objects.get(id=session['batch'])
        newSession = Sessions(course=courseToSave, batch=batchToSave,
                              sessionNumber=session['sessionNumber'], start_day=session['start_day'], end_day=session['end_day'])
        newSession.save()
    sessions = Sessions.objects.all()
    serializer = SessionSerializer(sessions, many=True)
    return Response({'status': 200, 'data': serializer.data})


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(username=username, password=password)
    if user.profile.type == 'coach':
        userProfile = Coach.objects.get(id=user.profile.id)
    elif user.profile.type == 'learner':
        userProfile = Learners.objects.get(id=user.profile.id)
    elif user.profile.type == 'faculty':
        userProfile = Faculty.objects.get(id=user.profile.id)
    elif user.profile.type == 'admin':
        userProfile = User.objects.get(id=user.profile.id)
    if user is not None:
        token = Token.objects.get_or_create(user=user)
        return Response({'status': '200', 'username': user.username, 'token': str(token[0]), 'email': userProfile.email, 'usertype': user.profile.type, "id": userProfile.id})

    return Response(status=401)


@api_view(['POST'])
@permission_classes([AllowAny])
def registerUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        newUser = User.objects.create_user(
            username=request.data['email'], email=request.data['email'], password=request.data['password'])
        newUser.save()
    else:
        return Response(status='403')
    user = User.objects.get(username=serializer.data['username'])
    userToSave = User.objects.get(username=serializer.data['email'])
    newProfile = Profile(user=userToSave, type="admin",
                         email=serializer.data['email'])
    newProfile.save()
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'status': 200, 'payload': serializer.data, 'token': str(token)})


@api_view(['POST'])
@permission_classes([AllowAny])
def addProfileType(request):
    serializer = ProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response({'status': '400 Bad request', 'Reason': 'Wrong data sent'})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def getProfile(request):
    session = Profile.objects.all()
    serializer = ProfileSerializer(session, many=True)
    return Response(serializer.data)

# getAvailableSlots
# [
#      { learnerId, batchId , weekId }
# ]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getAvailableSlots(request):
    bookedSlot = request.data
    print(bookedSlot)
    learner = Learners.objects.get(id=bookedSlot['learnerId'])
    batch = Batch.objects.get(id=bookedSlot['batchId'])
    week_id = bookedSlot['weekId']
    getReleventSlotsForThisBatch = DayTimeSlot.objects.filter(
        week_id=week_id,
        isConfirmed=True,
        coachcoachysession__isnull=True,
        for_learners=True
    )
    serializer = SlotTimeDaySerializer(getReleventSlotsForThisBatch, many=True)
    return Response({'status': 200, 'data': serializer.data})


#! Sample Input
# [
#    { slotId: 123, learnerId: 123, batchId: 2, !!(day: 'Monday', start_time_id: 121212121, end_time_id: 4185454554) },
# ]
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pickLearnerSlot(request):
    bookedSlot = request.data
    learner = Learners.objects.get(id=bookedSlot['learnerId'])
    batch = Batch.objects.get(id=bookedSlot['batchId'])
    slot = DayTimeSlot.objects.get(id=bookedSlot['slotId'])
    print(bookedSlot)
    newCoachCoachySession = CoachCoachySession(
        learner=learner, batch=batch, slot=slot)
    newCoachCoachySession.save()
    allSessionsForThisLearner = DayTimeSlot.objects.filter(
        coachcoachysession__learner=learner, isConfirmed=True)
    serializer = SlotTimeDaySerializer(allSessionsForThisLearner, many=True)
    return Response({'status': 200, 'data': serializer.data})


#! Sample Input
# [
#    { id: learner's id },
# ]
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getLearnerSlot(request):
    allSessionsForLearner = DayTimeSlot.objects.filter(
        ~Q(coachcoachysession=None),
        isConfirmed=True,
    )
    serializer = SlotTimeDaySerializer(allSessionsForLearner, many=True)
    return Response({'status': 200, 'data': serializer.data})


@api_view(['GET'])
@permission_classes([AllowAny])
def getCoachCoacheeSessions(request):
    print("hello")
    coachCoacheeSessions = CoachCoachySession.objects.all()
    serializer = CoachCoachySessionSerializer(coachCoacheeSessions, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def loginLearner(request):  # request.data = body
    email = request.data['email']
    user = User.objects.get(email=email)
    print(user.email)
    # link = reverse("trial")
    # link = request.build_absolute_uri(link)
    link = 'http://127.0.0.1:8000/trial/'
    link += get_query_string(user)
    print(link)
    return Response({"login": email})


@api_view(['GET'])
@permission_classes([AllowAny])
def trialLogin(request):
    sesame_id = request.GET.get('sesame', None)
    user = get_user(sesame_id)
    serializer = UserSerializer(user)
    print(serializer.data)
    return Response({"message": "hello"})
