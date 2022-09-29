from datetime import datetime
from email.message import EmailMessage
from multiprocessing import Event
import os
from django.core.mail import send_mail
from base.resources import ConfirmedSlotResource
from django.http import HttpResponse
from rest_framework.response import Response
from datetime import date
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from base.models import Coach, AdminRequest,  Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from pytz import timezone, utc
from base.models import SlotForCoach
from base.models import ConfirmedSlotsbyCoach
from base.models import Events
from base.models import LeanerConfirmedSlots
from .serializers import AdminReqSerializer, ConfirmedSlotsbyCoachSerializer, ConfirmedSlotsbyLearnerSerializer, EditUserSerializer, EventSerializer,  GetAdminReqSerializer,  CoachSerializer,  SlotForCoachSerializer,   UserSerializer, ProfileSerializer

from django.template.loader import render_to_string

# sesame
# from sesame.utils import get_query_string, get_user

# from sesame.utils import get_query_string, get_user

# flattening array
import uuid


# courses api functions

# @api_view(['GET'])
# @permission_classes([AllowAny])
# def getCourses(request):
#     courses = Courses.objects.all()
#     serializer = CourseSerializer(courses, many=True)
#     return Response(serializer.data)


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def addCourses(request):
#     serializer = CourseSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     else:
#         return Response({'status': '400 Bad request', 'Reason': 'Wrong data sent'})
#     return Response(serializer.data)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def updateCourses(request, _id):
#     course = Courses.objects.get(id=_id)
#     serializer = CourseSerializer(instance=course, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     else:
#         return Response({'status': '400 Bad request', 'Reason': 'Wrong data sent'})
#     return Response(serializer.data)


# @api_view(['GET'])
# @permission_classes([AllowAny])
# def getCourseCategory(request):
#     category = CourseCategorys.objects.all()
#     serializer = CourseCategorySerializer(category, many=True)
#     return Response(serializer.data)

# Learner Api Functions


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def getLearners(request):
#     learners = Learners.objects.all()
#     serializer = LearnerSerializer(learners, many=True)
#     return Response(serializer.data)


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def addLearners(request):
#     serializer = LearnerSerializer(data=request.data)
#     if serializer.is_valid():
#         newUser = User.objects.create_user(
#             username=request.data['email'], password='Meeraq@123')
#         newUser.save()
#         userToSave = User.objects.get(username=request.data['email'])
#         newProfile = Profile(user=userToSave, type="learner",
#                              email=request.data['email'])
#         newProfile.save()
#         serializer.save(user_id=newProfile.id)
#     for user in User.objects.all():
#         Token.objects.get_or_create(user=user)
#     return Response(serializer.data)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def updateLearners(request, _id):
#     learner = Learners.objects.get(id=_id)
#     serializer = LearnerSerializer(instance=learner, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)

# batch api


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def getBatches(request):
#     batches = Batch.objects.all()
#     serializer = BatchSerializer(batches, many=True)
#     return Response(serializer.data)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def addBatches(request):
#     serializer = BatchSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def updateBatches(request, _id):
#     batch = Batch.objects.get(id=_id)
#     serializer = BatchSerializer(instance=batch, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)


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
    email_message = render_to_string("addcoachmail.html", {
                                     'coach_name': request.data['first_name'], 'username': request.data['email'], 'password': request.data['password']})
    if serializer.is_valid():
        newUser = User.objects.create_user(
            username=request.data['email'], email=request.data['email'], password=request.data['password'])
        newUser.save()
        userToSave = User.objects.get(username=request.data['email'])
        newProfile = Profile(user=userToSave, type="coach",
                             email=request.data['email'])
        newProfile.save()
        serializer.save(user_id=newProfile.id)
        send_mail(
            # title:
            "You are added as Coach in {title}".format(title="Meeraq"),
            # message:
            email_message,
            # from:0
            "info@meeraq.com",
            # to:
            [request.data['email']],
            html_message=email_message
        )
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
    user = User.objects.get(username=coach.email)
    changedUser = {
        'username': request.data['email'],
        'email': request.data['email'],
    }
    editSerilizer = EditUserSerializer(instance=user, data=changedUser)
    if editSerilizer.is_valid():
        editSerilizer.save()
    serializer = CoachSerializer(instance=coach, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

# faculty api

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def getfaculty(request):
#     coaches = Faculty.objects.all()
#     serializer = FacultySerializer(coaches, many=True)
#     return Response(serializer.data)


# @api_view(['POST'])
# def addfaculty(request):
#     serializer = FacultySerializer(data=request.data)
#     if serializer.is_valid():
#         newUser = User.objects.create_user(
#             username=request.data['email'], password='Meeraq@123')
#         newUser.save()
#         userToSave = User.objects.get(username=request.data['email'])
#         newProfile = Profile(user=userToSave, type="faculty",
#                              email=request.data['email'])
#         newProfile.save()
#         serializer.save(user_id=newProfile.id)
#     else:
#         print(serializer.errors)
#         return Response(status='403')
#     for user in User.objects.all():
#         token = Token.objects.get_or_create(user=user)
#     return Response({'status': 200, 'payload': serializer.data, 'token': str(token[0])})


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def updateFaculty(request, _id):
#     faculty = Faculty.objects.get(id=_id)
#     serializer = FacultySerializer(instance=faculty, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)

# slot api


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def getslot(request):
#     slots = Slot.objects.all()
#     serializer = SlotSerializer(slots, many=True)
#     return Response(serializer.data)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def addslot(request):
#     serializer = SlotSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def getDayTimeslot(request):
#     slots = DayTimeSlot.objects.all()
#     serializer = SlotTimeDaySerializer(slots, many=True)
#     return Response(serializer.data)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def addDayTimeslot(request):
#     for eachDay in request.data:
#         coachToSave = Coach.objects.get(id=eachDay['coach'])
#         newdayTimeSlot = DayTimeSlot(
#             coach=coachToSave,
#             day=eachDay['day'],
#             start_time_id=eachDay['start_time_id'],
#             end_time_id=eachDay['end_time_id'],
#             week_id=eachDay['week_id']
#         )
#         newdayTimeSlot.save()

#     # only return the slots for the specific coach
#     slots = DayTimeSlot.objects.filter(coach=coachToSave)
#     serializer = SlotTimeDaySerializer(slots, many=True)
#     return Response({'status': 200, 'data': serializer.data})

# confirm day time slot


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def confirmDayTimeSlot(request):
#     for eachDay in request.data:
#         coachToSave = Coach.objects.get(id=eachDay['coach'])
#         newdayTimeSlot = DayTimeSlot(
#             coach=coachToSave,
#             day=eachDay['day'],
#             start_time_id=eachDay['start_time_id'],
#             end_time_id=eachDay['end_time_id'],
#             week_id=eachDay['week_id'],
#             isConfirmed=True
#         )
#         newdayTimeSlot.save()
#         currTime = int(eachDay['start_time_id'])
#         endTime = int(eachDay['end_time_id'])
#         while currTime + 1800000 <= endTime:
#             learnerSlot = DayTimeSlot(
#                 coach=coachToSave,
#                 day=eachDay['day'],
#                 start_time_id=str(currTime),
#                 end_time_id=str(currTime + 1800000),
#                 week_id=eachDay['week_id'],
#                 isConfirmed=True,
#                 for_learners=True
#             )
#             currTime += 2700000
#             learnerSlot.save()
#     # only return the confirmed slots for the specific coach
#     slots = DayTimeSlot.objects.filter(
#         coach=coachToSave, isConfirmed=True, for_learners=False)
#     serializer = SlotTimeDaySerializer(slots, many=True)
#     return Response({'status': 200, 'data': serializer.data})


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def updateDayTimeslot(request, _id):
#     slot = DayTimeSlot.objects.get(id=_id)
#     serializer = SlotTimeDaySerializer(instance=slot, data=request.data)
#     if serializer.is_valid():
#         serializer.save()

#     slots = DayTimeSlot.objects.all()
#     serializer = SlotTimeDaySerializer(slots, many=True)
#     return Response({'status': 200, 'data': serializer.data})


# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def deleteDayTimeslot(request, _id):
#     slot = DayTimeSlot.objects.get(id=_id)
#     slot.delete()

#     slots = DayTimeSlot.objects.all()
#     serializer = SlotTimeDaySerializer(slots, many=True)
#     return Response({'status': 200, 'data': serializer.data})

# # learner slot book


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def learnergetDayTimeslot(request):
#     slots = LearnerdayTimeSlot.objects.all()
#     serializer = LearnerSlotTimeDaySerializer(slots, many=True)
#     return Response(serializer.data)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def addLearnerDayTimeslot(request):
#     for day in request.data:
#         newdayTimeSlot = LearnerdayTimeSlot(
#             learner=day['learner'], start_time_id=day['start_time_id'], end_time_id=day['end_time_id'])
#         newdayTimeSlot.save()
#     slots = LearnerdayTimeSlot.objects.all()
#     serializer = LearnerSlotTimeDaySerializer(slots, many=True)
#     return Response({'status': 200, 'data': serializer.data})


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def updateLearnerDayTimeslot(request, _id):
#     slot = LearnerdayTimeSlot.objects.get(id=_id)
#     serializer = LearnerSlotTimeDaySerializer(instance=slot, data=request.data)
#     if serializer.is_valid():
#         serializer.save()

#     slots = LearnerdayTimeSlot.objects.all()
#     serializer = LearnerSlotTimeDaySerializer(slots, many=True)
#     return Response({'status': 200, 'data': serializer.data})


# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def LearnerdeleteDayTimeslot(request, _id):
#     slot = LearnerdayTimeSlot.objects.get(id=_id)
#     slot.delete()
#     slots = LearnerdayTimeSlot.objects.all()
#     serializer = LearnerSlotTimeDaySerializer(slots, many=True)
#     return Response({'status': 200, 'data': serializer.data})


# sessions


# @api_view(['GET'])
# @permission_classes([AllowAny])
# def getSessions(request):
#     session = Sessions.objects.all()
#     serializer = SessionSerializer(session, many=True)
#     return Response(serializer.data)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def addSession(request):
#     for session in request.data:
#         print(session)
#         courseToSave = Courses.objects.get(id=session['course'])
#         batchToSave = Batch.objects.get(id=session['batch'])
#         newSession = Sessions(course=courseToSave, batch=batchToSave,
#                               sessionNumber=session['sessionNumber'], start_day=session['start_day'], end_day=session['end_day'])
#         newSession.save()
#     sessions = Sessions.objects.all()
#     serializer = SessionSerializer(sessions, many=True)
#     return Response({'status': 200, 'data': serializer.data})


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        print(user)
        print(user.last_login)
        if user.profile.type == 'coach':
            userProfile = Coach.objects.get(email=username)
            token = Token.objects.get_or_create(user=user)
            return Response({'status': '200', 'username': user.username, 'first_name': userProfile.first_name, 'middle_name': userProfile.middle_name, 'last_name': userProfile.last_name, 'token': str(token[0]), 'email': userProfile.email, 'usertype': user.profile.type, "id": userProfile.id})
        # elif user.profile.type == 'learner':
        #     userProfile = Learners.objects.get(email=username)
        # elif user.profile.type == 'faculty':
        #     userProfile = Faculty.objects.get(email=username)
        elif user.profile.type == 'admin':
            userProfile = User.objects.get(email=username)
            token = Token.objects.get_or_create(user=user)
            return Response({'status': '200', 'username': user.username, 'token': str(token[0]), 'email': userProfile.email, 'usertype': user.profile.type, "id": userProfile.id})
        # token = Token.objects.get_or_create(user=user)
        # return Response({'status': '200', 'username': user.username, 'name': userProfile.name, 'token': str(token[0]), 'email': userProfile.email, 'usertype': user.profile.type, "id": userProfile.id})
    else:
        userFound = User.objects.filter(email=username)
        if userFound.exists():
            return Response({'reason': 'Invalid Password'}, status=401)
        else:
            return Response({'reason': 'No user found'}, status=404)


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
    user = User.objects.get(username=serializer.data['email'])
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


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def getAvailableSlots(request):
#     bookedSlot = request.data
#     print(bookedSlot)
#     learner = Learners.objects.get(id=bookedSlot['learnerId'])
#     batch = Batch.objects.get(id=bookedSlot['batchId'])
#     week_id = bookedSlot['weekId']
#     getReleventSlotsForThisBatch = DayTimeSlot.objects.filter(
#         week_id=week_id,
#         isConfirmed=True,
#         coachcoachysession__isnull=True,
#         for_learners=True
#     )
#     serializer = SlotTimeDaySerializer(getReleventSlotsForThisBatch, many=True)
#     return Response({'status': 200, 'data': serializer.data})


#! Sample Input
# [
#    { slotId: 123, learnerId: 123, batchId: 2, !!(day: 'Monday', start_time_id: 121212121, end_time_id: 4185454554) },
# ]
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def pickLearnerSlot(request):
#     bookedSlot = request.data
#     learner = Learners.objects.get(id=bookedSlot['learnerId'])
#     batch = Batch.objects.get(id=bookedSlot['batchId'])
#     slot = DayTimeSlot.objects.get(id=bookedSlot['slotId'])
#     print(bookedSlot)
#     newCoachCoachySession = CoachCoachySession(
#         learner=learner, batch=batch, slot=slot)
#     newCoachCoachySession.save()
#     allSessionsForThisLearner = DayTimeSlot.objects.filter(
#         coachcoachysession__learner=learner, isConfirmed=True)
#     serializer = SlotTimeDaySerializer(allSessionsForThisLearner, many=True)
#     return Response({'status': 200, 'data': serializer.data})


#! Sample Input
# [
#    { id: learner's id },
# ]
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def getLearnerSlot(request):
#     allSessionsForLearner = DayTimeSlot.objects.filter(
#         ~Q(coachcoachysession=None),
#         isConfirmed=True,
#     )
#     serializer = SlotTimeDaySerializer(allSessionsForLearner, many=True)
#     return Response({'status': 200, 'data': serializer.data})


# @api_view(['GET'])
# @permission_classes([AllowAny])
# def getCoachCoacheeSessions(request):
#     print("hello")
#     coachCoacheeSessions = CoachCoachySession.objects.all()
#     serializer = CoachCoachySessionSerializer(coachCoacheeSessions, many=True)
#     return Response(serializer.data)


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def loginLearner(request):  # request.data = body
#     email = request.data['email']
#     user = User.objects.get(email=email)
#     print(user.email)
#     # link = reverse("trial")
#     # link = request.build_absolute_uri(link)
#     link = 'http://127.0.0.1:8000/trial/'
#     link += get_query_string(user)
#     print(link)
#     return Response({"login": email})


# @api_view(['GET'])
# @permission_classes([AllowAny])
# def trialLogin(request):
#     sesame_id = request.GET.get('sesame', None)
#     user = get_user(sesame_id)
#     serializer = UserSerializer(user)
#     print(serializer.data)
#     return Response({"message": "hello"})

# from django.template.loader import get_template


@api_view(['POST'])
@permission_classes([AllowAny])
def makeSlotRequest(request):
    adminRequest = AdminRequest(
        name=request.data['request_name'], expire_date=request.data['expiry_date'])
    adminRequest.save()
    for coach in request.data['coach_id']:
        single_coach = Coach.objects.get(id=coach)
        email_message = render_to_string("makerequest.html", {
                                         'expire_date': request.data['expiry_date'], 'coach_name': single_coach.first_name})

        send_mail(
            # title:
            "Meeraq - Coaching Sessions Slot Requests",
            # message:
            email_message,
            # from:0
            "info@meeraq.com",
            # to:
            [single_coach.email],
            html_message=email_message
        )
        adminRequest.assigned_coach.add(single_coach)
    for slot in request.data['slots']:
        newSlot = SlotForCoach(
            start_time=slot['start_time'],
            end_time=slot['end_time'],
            date=slot['date'],
            request=adminRequest
        )
        newSlot.save()
    return Response({'details': 'success'}, status=200)


@api_view(['GET'])
@permission_classes([AllowAny])
def getAdminRequestData(request):
    today = date.today()
    adminRequest = AdminRequest.objects.all()

    # killing the request by changing isActive field
    for _request in adminRequest:
        if today > _request.expire_date:
            newData = {
                'isActive': False,
                'expire_date': _request.expire_date,
                'name': _request.name,
            }
            newReq = AdminRequest.objects.filter(
                expire_date=_request.expire_date).first()
            adminSerializer = AdminReqSerializer(instance=newReq, data=newData)
            if adminSerializer.is_valid():
                adminSerializer.save()
            else:
                print(adminSerializer.errors)
    req = AdminRequest.objects.all()
    serilizedData = GetAdminReqSerializer(req, many=True)
    return Response({'details': 'success', 'Data': serilizedData.data}, status=200)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def deleteRequest(request, req_id):
    all_slots = SlotForCoach.objects.filter(request=req_id)
    for slot in all_slots:
        slot.delete()
    coach_slots = ConfirmedSlotsbyCoach.objects.filter(request_ID=req_id)
    for slot in coach_slots:
        slot.delete()
    req = AdminRequest.objects.get(id=req_id)
    req.delete()

    return Response({'status': 'success, Data deleted'}, status=200)


def checkIfCoachExistsInQuerySet(querySet, id):
    for coach in querySet:
        if (int(coach.id) == int(id)):
            return True
    return False


@api_view(['GET'])
@permission_classes([AllowAny])
def getSlotofRequest(request, coach_id, type):
    today = date.today()
    adminRequest = AdminRequest.objects.filter(assigned_coach__id=coach_id)

    # killing the request by changing isActive field
    for _request in adminRequest:
        if today > _request.expire_date:
            newData = {
                'isActive': False,
                'expire_date': _request.expire_date,
                'name': _request.name,
            }
            newReq = AdminRequest.objects.filter(
                expire_date=_request.expire_date).first()
            adminSerializer = AdminReqSerializer(instance=newReq, data=newData)
            if adminSerializer.is_valid():
                adminSerializer.save()
            else:
                print(adminSerializer.errors)
    request_id_name = {}
    all_slots = []

    for _request in adminRequest:
        confirmedCoaches = _request.confirmed_coach.all()
        if type == 'NEW':
            if _request.isActive == True and (not checkIfCoachExistsInQuerySet(confirmedCoaches, coach_id)):
                request_id_name[_request.id] = _request.name
                all_slots += (SlotForCoach.objects.filter(request=_request))
        if type == "ACTIVE":
            if _request.isActive == True and checkIfCoachExistsInQuerySet(confirmedCoaches, coach_id):
                request_id_name[_request.id] = _request.name
                all_slots += (SlotForCoach.objects.filter(request=_request))
        if type == "PAST":
            if _request.isActive == False and checkIfCoachExistsInQuerySet(confirmedCoaches, coach_id):
                request_id_name[_request.id] = _request.name
                all_slots += (SlotForCoach.objects.filter(request=_request))
        if type == "MISSED":
            if _request.isActive == False and (not checkIfCoachExistsInQuerySet(confirmedCoaches, coach_id)):
                request_id_name[_request.id] = _request.name
                all_slots += (SlotForCoach.objects.filter(request=_request))

    serializers = SlotForCoachSerializer(all_slots, many=True)
    return Response({'details': 'success', 'slots': serializers.data, 'requests': request_id_name}, status=200)


@api_view(['POST'])
@permission_classes([AllowAny])
def confirmAvailableSlotsByCoach(request, coach_id, request_id):
    for slot in request.data:
        start_timestamp = (int(slot['start_time'])/1000) + 19800
        end_timestamp = (int(slot['end_time'])/1000) + 19800
        newSlot = ConfirmedSlotsbyCoach(
            start_time=slot['start_time'],
            end_time=slot['end_time'],
            date=slot['date'],
            coach_id=coach_id,
            request_ID=int(request_id),
            SESSION_START_TIME=datetime.fromtimestamp(
                start_timestamp).strftime('%I:%M %p'),
            SESSION_END_TIME=datetime.fromtimestamp(
                end_timestamp).strftime('%I:%M %p'),
            SESSION_DATE=datetime.fromtimestamp(
                int(start_timestamp)).strftime('%d %B %Y'),
            COACH_NAME=Coach.objects.get(id=coach_id).first_name + " " + Coach.objects.get(
                id=coach_id).middle_name + " " + Coach.objects.get(id=coach_id).last_name,
            DESCRIPTION=AdminRequest.objects.get(id=request_id).name,
            CC=Coach.objects.get(id=coach_id).email,
            MEETING_LINK=Coach.objects.get(id=coach_id).meet_link
        )
        newSlot.save()
    coach = Coach.objects.get(id=coach_id)
    adminRequest = AdminRequest.objects.get(id=request_id)
    adminRequest.confirmed_coach.add(coach)
    return Response({'details': 'success'}, status=200)


# Create your views here.


@api_view(['GET'])
@permission_classes([AllowAny])
def export(request, request_id):
    coach_slot_file = ConfirmedSlotResource()
    dataset = coach_slot_file.export(
        ConfirmedSlotsbyCoach.objects.filter(request_ID=request_id))
    response = HttpResponse(
        dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="slots.xls"'
    return response


@api_view(['GET'])
@permission_classes([AllowAny])
def export_all(request):
    today = date.today()
    coach_slot_file = ConfirmedSlotResource()
    dataset = coach_slot_file.export(ConfirmedSlotsbyCoach.objects.all())
    response = HttpResponse(
        dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="allslots.xls"'
    return response


@api_view(['GET'])
@permission_classes([AllowAny])
def getConfirmedSlotsbyCoach(request, coach_id):
    slot = ConfirmedSlotsbyCoach.objects.filter(coach_id=coach_id)
    serializer = ConfirmedSlotsbyCoachSerializer(slot, many=True)
    return Response({'details': 'success', 'data': serializer.data}, status=200)


@api_view(['GET'])
@permission_classes([AllowAny])
def getConfirmedSlotsbyRequestID(request, req_id):
    slot = ConfirmedSlotsbyCoach.objects.filter(request_ID=req_id)
    serializer = ConfirmedSlotsbyCoachSerializer(slot, many=True)
    return Response({'details': 'success', 'data': serializer.data}, status=200)


@api_view(['POST'])
@permission_classes([AllowAny])
def updateConfirmedSlots(request, slot_id):
    slot = ConfirmedSlotsbyCoach.objects.filter(id=slot_id).first()
    serializer = ConfirmedSlotsbyCoachSerializer(
        instance=slot, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response({'details': 'success', 'data': serializer.data}, status=201)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def deleteConfirmedSlotsbyCoach(request, coach_id, slot_id):
    slot = ConfirmedSlotsbyCoach.objects.get(id=slot_id)
    slot.delete()
    all_slots = ConfirmedSlotsbyCoach.objects.filter(coach_id=coach_id)
    serializer = ConfirmedSlotsbyCoachSerializer(all_slots, many=True)
    return Response({'status': 'success, Data deleted', 'data': serializer.data}, status=200)


# update meet link by coach

@api_view(['POST'])
@permission_classes([AllowAny])
def updateMeetLinkByCoach(request, _id):
    coach = Coach.objects.get(id=_id)
    user = User.objects.get(email=coach.email)
    newMeetLink = {
        'user': user,
        'first_name': coach.first_name,
        'middle_name': coach.middle_name,
        'last_name': coach.last_name,
        'email': coach.email,
        'phone': coach.phone,
        'dob': coach.dob,
        'gender': coach.gender,
        'fee': coach.fee,
        'activeSince': coach.activeSince,
        'isSlotBooked': coach.isSlotBooked,
        'isActive': coach.isActive,
        'meet_link': request.data['meet_link']
    }
    serializer = CoachSerializer(instance=coach, data=newMeetLink)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def addEvent(request):
    event_id = uuid.uuid1()
    event_data = {
        'name':request.data['name'],
        'start_date':request.data['start_date'],
        'end_date':request.data['end_date'],
        'expire_date':request.data['expire_date'],
        'count':request.data['count'],
        'link':'https://slots.meeraq.com/' + str(event_id) + '/',
        '_id':str(event_id),
        'coach':request.data['coach']
    }
    serializer = EventSerializer(data = event_data)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)
        return Response({'status': '400 Bad request', 'reason': 'Wrong data sent'}, status=400)
    return Response(status = 201)

@api_view(['GET'])
@permission_classes([AllowAny])
def getEvents(request):
    events = Events.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response({'status': 'success', 'data': serializer.data}, status=200)

@api_view(['POST'])
@permission_classes([AllowAny])
def editEvents(request,event_id):
    event = Events.objects.get(id=event_id)
    event_data = {
        'name':request.data['name'],
        'start_date':event.start_date,
        'end_date':request.data['end_date'],
        'expire_date':request.data['expire_date'],
        'count':request.data['count'],
        'link':event.link,
        '_id':event._id,
        'coach':request.data['coach']
    }
    serializer = EventSerializer(instance=event, data=event_data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response({'status': '400 Bad request', 'reason': 'Wrong data sent'}, status=400)
    return Response({'status': 'success', 'data': serializer.data}, status=200)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def deleteEvents(request, event_id):
    event = Events.objects.get(id=event_id)
    event.delete()
    return Response({'status': 'success, Data deleted'}, status=200)




@api_view(['GET'])
@permission_classes([AllowAny])
def getSlotsByEventID(request, event_id):
    event = Events.objects.get(_id=event_id)
    all_slots = []
    for coach in event.coach.all():
        slots = ConfirmedSlotsbyCoach.objects.filter(coach_id=coach.id)
        for slot in slots:
            if slot.is_confirmed == False & slot.is_realeased == False:
                all_slots.append(slot)
    serializer = ConfirmedSlotsbyCoachSerializer(all_slots, many=True)
    eventserializer = EventSerializer(event)
    return Response({'status': 'success','slots':serializer.data,'event':eventserializer.data}, status=200)




def createIcs(start_time,end_time):
    fp = open('event.ics', 'w')
    fp.write('BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//hacksw/handcal//NONSGML v1.0//EN\nBEGIN:VEVENT\nUID:uid1@example.com\nDTSTAMP:20221014T170000Z\nORGANIZER;CN=Nishant:MAILTO:nishant@meeraq.com\nDTSTART:'+start_time+'\nDTEND:20221015T035959Z'+end_time+'nSUMMARY:Meeraq | Coaching Session \nLOCATION:https://www.google.com/\nGEO:48.85299;2.36885\nEND:VEVENT\nEND:VCALENDAR')
    fp.close()


@api_view(['POST'])
@permission_classes([AllowAny])
def confirmSlotsByLearner(request,slot_id):
    coach_slot = ConfirmedSlotsbyCoach.objects.get(id=slot_id)
    
    booked_slot_coach = {
        **coach_slot,
        'is_confirmed': True
    }
    coach_serilizer = ConfirmedSlotsbyCoachSerializer(instance=coach_slot,data = booked_slot_coach)
    Booked_slot = {
        'name':request.data['name'],
        'email':request.data['email'],
        'organisation':request.data['organisation'],
        'phone_no':request.data['phone_no'],
        'slot':coach_slot.id,
        'event':request.data['event']
    }
    event = Events.objects.get(id=request.data['event'])
    count = int(event.count)
    coach_ids = []
    for coach in event.coach.all():
        coach_ids.append(coach.id)
    new_count = count-1
    new_event_data = {
        'name':event.name,
        'start_date':event.start_date,
        'end_date':event.end_date,
        'expire_date':event.expire_date,
        'count':str(new_count),
        'link':event.link,
        '_id':event._id,
        'coach':coach_ids
    }
    event_serializer = EventSerializer(instance=event, data=new_event_data)
    if event_serializer.is_valid():
        event_serializer.save()
    else:
        print(event_serializer.errors)

    serializer = ConfirmedSlotsbyLearnerSerializer(data = Booked_slot)
    if serializer.is_valid():
        booked_slots = LeanerConfirmedSlots.objects.all()
        if request.data['warning'] == True:
            for slot in booked_slots:
                if (slot.email == request.data['email']) & (request.data['event'] == slot.event.id):
                    return Response({'status': '409 Bad request', 'reason': 'email already exist'}, status=409)
                else:
                    serializer.save()
                    if event_serializer.is_valid():
                        event_serializer.save()
                    else:
                        print(event_serializer.errors)
        else:
            serializer.save()
            if event_serializer.is_valid():
                event_serializer.save()
            else:
                print(event_serializer.errors)
    else:
        return Response({'status': '400 Bad request', 'reason': 'wrong data sent'}, status=400)

    if coach_serilizer.is_valid():
        coach_serilizer.save()
    else:
        return Response({'status': '400 Bad request', 'reason': 'coach data is wrong'}, status=400)

    start =(coach_slot.start_time.replace(microsecond=0).astimezone(utc).replace(tzinfo=None).isoformat() + 'Z').replace(':','').replace('-','')
    end = (coach_slot.end_time.replace(microsecond=0).astimezone(utc).replace(tzinfo=None).isoformat() + 'Z').replace(':','').replace('-','')
    createIcs(start,end)
    email = EmailMessage(
        'Subject',
        'Email body',
        'info@meeraq.com',
        ['yaswanth@meeraq.com', 'pankaj@meeraq.com']
    )
    email.attach_file('event.ics', 'text/calendar')
    email.send()
    if os.path.exists("event.ics"):
        os.remove("event.ics")
    else:
        print('file not found')
    return Response({'status': 'success', 'data': serializer.data}, status=200)
    


@api_view(['GET'])
@permission_classes([AllowAny])
def getConfirmSlotsByLearner(request):
    booked_slots = LeanerConfirmedSlots.objects.all()
    serializer = ConfirmedSlotsbyLearnerSerializer(booked_slots, many=True)
    return Response({'status': 'success','data':serializer.data}, status=200)


@api_view(['GET'])
@permission_classes([AllowAny])
def getConfirmSlotsByLearnerByEventId(request,event_id):
    booked_slots = LeanerConfirmedSlots.objects.filter(event = event_id)
    serializer = ConfirmedSlotsbyLearnerSerializer(booked_slots, many=True)
    return Response({'status': 'success','data':serializer.data}, status=200)