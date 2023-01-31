import uuid
from django.template.loader import render_to_string
import jwt
from datetime import datetime, time, timedelta
from django.core.mail import EmailMessage
import os
from django.core.mail import send_mail
from base.resources import ConfirmedSlotResource, LearnerConfirmedSlotsResource
from django.http import HttpResponse
from rest_framework.response import Response
from datetime import date
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from base.models import Coach, AdminRequest, Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from pytz import utc
from base.models import SlotForCoach
from base.models import ConfirmedSlotsbyCoach
from base.models import Events
from base.models import LeanerConfirmedSlots, CoachPrice
# ServiceApprovalData  # ServiceApprovalEntry
from base.models import Batch, Learner, DeleteConfirmedSlotsbyAdmin, ServiceApproval
from base.models import PurchaseOrder, Rejected
from .serializers import (
    AdminReqSerializer,
    PurchaseOrderDepthOneSerializer,
    ServiceApprovalSerializer,
    CoachPriceSerializer,
    BatchSerializer,
    LearnerSerializerInDepthSerializer,
    # ServiceApprovalEntrySerializer,
    ServiceApprovalDepthOneSerializer,
    ServiceApprovalDepthTwoSerializer,
    ConfirmedLearnerSerializer,
    ConfirmedSlotsbyCoachSerializer,
    ConfirmedSlotsbyLearnerSerializer,
    EditUserSerializer,
    EventSerializer,
    GetAdminReqSerializer,
    CoachSerializer,
    LearnerDataUploadSerializer,
    SlotForCoachSerializer,
    UserSerializer,
    ProfileSerializer,
    LoginUserSerializer,
    DeletedConfirmedSlotsSerializer,
    GetNestedDeletedConfirmedSlotsSerializer,
    CoachPriceSerializer,
    EventDepthOneSerializer,
    PurchaseOrderSerializer,
    RejectedSerializer
)

import environ
env = environ.Env()
environ.Env.read_env()

# sesame
# from sesame.utils import get_query_string, get_user

# from sesame.utils import get_query_string, get_user

# flattening array


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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getcoach(request):
    coaches = Coach.objects.all()
    serializer = CoachSerializer(coaches, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([AllowAny])
def addcoach(request):
    serializer = CoachSerializer(data=request.data)
    email_message = render_to_string(
        "addcoachmail.html",
        {
            "coach_name": request.data["first_name"],
            "username": request.data["email"],
            "password": request.data["password"],
            "coach_url": env("coach_url")
        },
    )
    if serializer.is_valid():
        newUser = User.objects.create_user(
            username=request.data["email"], email=request.data["email"], password=request.data["password"]
        )
        newUser.save()
        userToSave = User.objects.get(username=request.data["email"])
        newProfile = Profile(user=userToSave, type="coach",
                             email=request.data["email"])
        newProfile.save()
        serializer.save(user_id=newProfile.id)
        send_mail(
            # title:
            "You are added as a Coach on {title}".format(title="Meeraq"),
            # message:
            email_message,
            # from:0
            "info@mail.meeraq.com",
            # to:
            [request.data["email"]],
            html_message=email_message,
        )
        for user in User.objects.all():
            token = Token.objects.get_or_create(user=user)
    else:
        print(serializer.errors)
        return Response(status="403")
    return Response({"status": 200, "payload": serializer.data, "token": str(token[0])})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def updateCoach(request, _id):
    coach = Coach.objects.get(id=_id)
    user = User.objects.get(username=coach.email)
    changedUser = {
        "username": request.data["email"],
        "email": request.data["email"],
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

def updateLastLogin(email):
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user = User.objects.get(username=email)
    changedUser = {
        "email": user.email,
        'last_login': today
    }
    editSerilizer = LoginUserSerializer(instance=user, data=changedUser)
    if editSerilizer.is_valid():
        editSerilizer.save()


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data["username"]
    password = request.data["password"]
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.profile.type == "coach":
            if request.data['type'] == 'coach':
                userProfile = Coach.objects.get(email=username)
                token = Token.objects.get_or_create(user=user)
                updateLastLogin(user.email)
                return Response(
                    {
                        "status": "200",
                        "username": user.username,
                        "first_name": userProfile.first_name,
                        "middle_name": userProfile.middle_name,
                        "last_name": userProfile.last_name,
                        "token": str(token[0]),
                        "email": userProfile.email,
                        "usertype": user.profile.type,
                        "id": userProfile.id,
                        "meet_link": userProfile.meet_link,
                        "last_login": user.last_login
                    }
                )
            else:
                return Response({"reason": "No user found"}, status=404)
        elif user.profile.type == "admin":
            if request.data['type'] == 'admin':
                userProfile = User.objects.get(email=username)
                token = Token.objects.get_or_create(user=user)
                updateLastLogin(user.email)
                return Response(
                    {
                        "status": "200",
                        "username": user.username,
                        "token": str(token[0]),
                        "email": userProfile.email,
                        "usertype": user.profile.type,
                        "id": userProfile.id,
                        "last_login": user.last_login
                    }
                )
        elif user.profile.type == "finance":
            if request.data['type'] == 'finance':
                userProfile = User.objects.get(email=username)
                token = Token.objects.get_or_create(user=user)
                updateLastLogin(user.email)
                return Response(
                    {
                        "status": "200",
                        "username": user.username,
                        "token": str(token[0]),
                        "email": userProfile.email,
                        "usertype": user.profile.type,
                        "id": userProfile.id,
                        "last_login": user.last_login
                    }
                )
            else:
                return Response({"reason": "No user found"}, status=404)

    else:
        userFound = User.objects.filter(email=username)
        if userFound.exists():
            return Response({"reason": "Invalid Password"}, status=401)
        else:
            return Response({"reason": "No user found"}, status=404)


@api_view(["POST"])
@permission_classes([AllowAny])
def registerUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        newUser = User.objects.create_user(
            username=request.data["email"], email=request.data["email"], password=request.data["password"]
        )
        newUser.save()
    else:
        return Response(status="403")
    user = User.objects.get(username=serializer.data["email"])
    userToSave = User.objects.get(username=serializer.data["email"])
    newProfile = Profile(user=userToSave, type="admin",
                         email=serializer.data["email"])
    newProfile.save()
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"status": 200, "payload": serializer.data, "token": str(token)})


@api_view(["POST"])
@permission_classes([AllowAny])
def addProfileType(request):
    serializer = ProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response({"status": "400 Bad request", "Reason": "Wrong data sent"})
    return Response(serializer.data)


@api_view(["GET"])
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


@api_view(["POST"])
@permission_classes([AllowAny])
def makeSlotRequest(request):
    adminRequest = AdminRequest(
        name=request.data["request_name"], expire_date=request.data["expiry_date"], end_date=request.data['end_date'], start_date=request.data['start_date'])
    adminRequest.save()
    for coach in request.data["coach_id"]:
        single_coach = Coach.objects.get(id=coach)
        email_message = render_to_string(
            "makerequest.html", {
                "expire_date": request.data["expiry_date"], "coach_name": single_coach.first_name, "coach_url": env("coach_url")}
        )

        send_mail(
            # title:
            "Meeraq - Coaching Sessions Slot Requests",
            # message:
            email_message,
            # from:0
            "info@meeraq.com",
            # to:
            [single_coach.email],
            html_message=email_message,
        )
        adminRequest.assigned_coach.add(single_coach)
    for slot in request.data["slots"]:
        newSlot = SlotForCoach(
            start_time=slot["start_time"], end_time=slot["end_time"], date=slot["date"], request=adminRequest
        )
        newSlot.save()
    return Response({"details": "success"}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getAdminRequestData(request):
    today = date.today()
    adminRequest = AdminRequest.objects.all()

    # killing the request by changing isActive field
    for _request in adminRequest:
        if today > _request.expire_date:
            newData = {
                "isActive": False,
                "expire_date": _request.expire_date,
                "name": _request.name,
            }
            # newReq = AdminRequest.objects.filter(
            #     expire_date=_request.expire_date).first()
            newReq = AdminRequest.objects.get(id=_request.id)
            adminSerializer = AdminReqSerializer(instance=newReq, data=newData)
            if adminSerializer.is_valid():
                adminSerializer.save()
            else:
                print(adminSerializer.errors)
    countOfSlotsPerRequest = {}
    req = AdminRequest.objects.all()
    for reqItem in req:
        slotsPerReq = ConfirmedSlotsbyCoach.objects.filter(
            request_ID=reqItem.id)
        countOfSlotsPerRequest[reqItem.id] = len(slotsPerReq)
    serilizedData = GetAdminReqSerializer(req, many=True)
    return Response({"details": "success", "Data": serilizedData.data, "countOfSlotsPerRequest": countOfSlotsPerRequest}, status=200)


@api_view(["DELETE"])
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

    return Response({"status": "success, Data deleted"}, status=200)


def checkIfCoachExistsInQuerySet(querySet, id):
    for coach in querySet:
        if int(coach.id) == int(id):
            return True
    return False


@api_view(["GET"])
@permission_classes([AllowAny])
def getSlotofRequest(request, coach_id, type):
    today = date.today()
    adminRequest = AdminRequest.objects.filter(assigned_coach__id=coach_id)

    # killing the request by changing isActive field
    for _request in adminRequest:
        if today > _request.expire_date:
            newData = {
                "isActive": False,
                "expire_date": _request.expire_date,
                "name": _request.name,
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
        if type == "NEW":
            if _request.isActive == True and (not checkIfCoachExistsInQuerySet(confirmedCoaches, coach_id)):
                request_id_name[_request.id] = _request.name
                all_slots += SlotForCoach.objects.filter(request=_request)
        if type == "ACTIVE":
            if _request.isActive == True and checkIfCoachExistsInQuerySet(confirmedCoaches, coach_id):
                request_id_name[_request.id] = _request.name
                all_slots += SlotForCoach.objects.filter(request=_request)
        if type == "PAST":
            if _request.isActive == False and checkIfCoachExistsInQuerySet(confirmedCoaches, coach_id):
                request_id_name[_request.id] = _request.name
                all_slots += SlotForCoach.objects.filter(request=_request)
        if type == "MISSED":
            if _request.isActive == False and (not checkIfCoachExistsInQuerySet(confirmedCoaches, coach_id)):
                request_id_name[_request.id] = _request.name
                all_slots += SlotForCoach.objects.filter(request=_request)

    serializers = SlotForCoachSerializer(all_slots, many=True)
    return Response({"details": "success", "slots": serializers.data, "requests": request_id_name}, status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
def confirmAvailableSlotsByCoach(request, coach_id, request_id):
    for slot in request.data:
        start_timestamp = (int(slot["start_time"]) / 1000) + 19800
        end_timestamp = (int(slot["end_time"]) / 1000) + 19800
        newSlot = ConfirmedSlotsbyCoach(
            start_time=slot["start_time"],
            end_time=slot["end_time"],
            date=slot["date"],
            coach_id=coach_id,
            request_ID=int(request_id),
            SESSION_START_TIME=datetime.fromtimestamp(
                start_timestamp).strftime("%I:%M %p"),
            SESSION_END_TIME=datetime.fromtimestamp(
                end_timestamp).strftime("%I:%M %p"),
            SESSION_DATE=datetime.fromtimestamp(
                int(start_timestamp)).strftime("%d %B %Y"),
            COACH_NAME=Coach.objects.get(id=coach_id).first_name
            + " "
            + Coach.objects.get(id=coach_id).middle_name
            + " "
            + Coach.objects.get(id=coach_id).last_name,
            DESCRIPTION=AdminRequest.objects.get(id=request_id).name,
            CC=Coach.objects.get(id=coach_id).email,
            MEETING_LINK=Coach.objects.get(id=coach_id).meet_link,
        )
        newSlot.save()
    coach = Coach.objects.get(id=coach_id)
    adminRequest = AdminRequest.objects.get(id=request_id)
    adminRequest.confirmed_coach.add(coach)
    return Response({"details": "success"}, status=200)


# Create your views here.


@api_view(["GET"])
@permission_classes([AllowAny])
def export(request, request_id):
    coach_slot_file = ConfirmedSlotResource()
    dataset = coach_slot_file.export(
        ConfirmedSlotsbyCoach.objects.filter(request_ID=request_id))
    response = HttpResponse(
        dataset.xls, content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = 'attachment; filename="slots.xls"'
    return response


@api_view(["GET"])
@permission_classes([AllowAny])
def export_all(request):
    today = date.today()
    coach_slot_file = ConfirmedSlotResource()
    dataset = coach_slot_file.export(ConfirmedSlotsbyCoach.objects.all())
    response = HttpResponse(
        dataset.xls, content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = 'attachment; filename="allslots.xls"'
    return response


@api_view(["GET"])
@permission_classes([AllowAny])
def getConfirmedSlotsbyCoach(request, coach_id):
    slot = ConfirmedSlotsbyCoach.objects.filter(coach_id=coach_id)
    serializer = ConfirmedSlotsbyCoachSerializer(slot, many=True)
    return Response({"details": "success", "data": serializer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getConfirmedSlotsbyRequestID(request, req_id):
    slot = ConfirmedSlotsbyCoach.objects.filter(request_ID=req_id)
    serializer = ConfirmedSlotsbyCoachSerializer(slot, many=True)
    return Response({"details": "success", "data": serializer.data}, status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
def updateConfirmedSlots(request, slot_id):
    slot = ConfirmedSlotsbyCoach.objects.filter(id=slot_id).first()
    start_timestamp = ((request.data["start_time"]) / 1000) + 19800
    end_timestamp = ((request.data["end_time"]) / 1000) + 19800
    print(str(request.data['start_time']),
          type(str(request.data['start_time'])))
    newSlot = {
        "start_time": request.data['start_time'],
        "end_time": request.data["end_time"],
        "date": request.data["date"],
        "coach_id": slot.coach_id,
        "request_ID": int(slot.request_ID),
        "SESSION_START_TIME": datetime.fromtimestamp(
            start_timestamp).strftime("%I:%M %p"),
        "SESSION_END_TIME": datetime.fromtimestamp(
            end_timestamp).strftime("%I:%M %p"),
        "SESSION_DATE": datetime.fromtimestamp(
            start_timestamp).strftime("%d %B %Y"),
        "COACH_NAME": Coach.objects.get(id=slot.coach_id).first_name
        + " "
        + Coach.objects.get(id=slot.coach_id).middle_name
        + " "
        + Coach.objects.get(id=slot.coach_id).last_name,
        "DESCRIPTION": AdminRequest.objects.get(id=slot.request_ID).name,
        "CC": Coach.objects.get(id=slot.coach_id).email,
        "MEETING_LINK": Coach.objects.get(id=slot.coach_id).meet_link,
    }

    serializer = ConfirmedSlotsbyCoachSerializer(
        instance=slot, data=newSlot)
    if serializer.is_valid():
        serializer.save()
    return Response({"details": "success", "data": serializer.data}, status=201)


@api_view(["DELETE"])
@permission_classes([AllowAny])
def deleteConfirmedSlotsbyCoach(request, coach_id, slot_id):
    slot = ConfirmedSlotsbyCoach.objects.get(id=slot_id)
    slot.delete()
    all_slots = ConfirmedSlotsbyCoach.objects.filter(coach_id=coach_id)
    serializer = ConfirmedSlotsbyCoachSerializer(all_slots, many=True)
    return Response({"status": "success, Data deleted", "data": serializer.data}, status=200)


# update meet link by coach


@api_view(["POST"])
@permission_classes([AllowAny])
def updateMeetLinkByCoach(request, _id):
    coach = Coach.objects.get(id=_id)
    user = User.objects.get(email=coach.email)
    newMeetLink = {
        "user": user,
        "first_name": coach.first_name,
        "middle_name": coach.middle_name,
        "last_name": coach.last_name,
        "email": coach.email,
        "phone": coach.phone,
        "dob": coach.dob,
        "gender": coach.gender,
        "fee": coach.fee,
        "activeSince": coach.activeSince,
        "isSlotBooked": coach.isSlotBooked,
        "isActive": coach.isActive,
        "meet_link": request.data["meet_link"],
    }
    serializer = CoachSerializer(instance=coach, data=newMeetLink)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)
    return Response(serializer.data)


def addCoachPrice(arrOfPrice):
    coach_price_id = []
    for arrData in arrOfPrice:
        try:
            if_in_coachprice_table = CoachPrice.objects.get(
                coach=arrData['coach'], price=arrData['price'])
            coach_price_id.append(if_in_coachprice_table.id)
        except:
            new_data = CoachPriceSerializer(data=arrData)
            if new_data.is_valid():
                instance = new_data.save()
                coach_price_id.append(instance.id)
    return coach_price_id


@api_view(["POST"])
@permission_classes([AllowAny])
def addEvent(request):
    event_id = uuid.uuid1()
    price_arr = addCoachPrice(request.data['coach_pricing'])
    event_data = {
        "name": request.data["name"],
        "start_date": request.data["start_date"],
        "end_date": request.data["end_date"],
        "expire_date": request.data["expire_date"],
        "count": request.data["count"],
        "min_count": request.data["count"],
        "link": env("learner_url") + "book-slot/" + str(event_id) + "/",
        "_id": str(event_id),
        "coach": request.data["coach"],
        "batch": request.data["batch"],
        "coach_price": price_arr
    }
    serializer = EventSerializer(data=event_data)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)
        return Response({"status": "400 Bad request", "reason": "Wrong data sent"}, status=400)
    return Response(status=201)


@api_view(["GET"])
@permission_classes([AllowAny])
def getEvents(request):
    today = date.today()
    events = Events.objects.all()
    for event in events:
        if event.expire_date < today:
            event_query_to_dict = EventSerializer(event)
            new_event = {**event_query_to_dict.data, "is_expired": True}
            event_serilizer = EventSerializer(instance=event, data=new_event)
            if event_serilizer.is_valid():
                event_serilizer.save()
            else:
                print(event_serilizer.errors)
                return Response({"status": "error", "reason": "error in expire event"}, status=401)
    updated_events = Events.objects.filter(is_delete=False)
    countOfConfirmedSessionsPerEvent = {}
    for event in updated_events:
        slotsPerEvent = LeanerConfirmedSlots.objects.filter(event__id=event.id)
        countOfConfirmedSessionsPerEvent[event.id] = len(slotsPerEvent)
    serializer = EventDepthOneSerializer(updated_events, many=True)
    return Response({"status": "success", "data": serializer.data, "countOfConfirmedSessionsPerEvent": countOfConfirmedSessionsPerEvent}, status=200)


@api_view(['GET'])
@permission_classes([AllowAny])
def getEventsAndSlotsByBatch(request, batch):
    events = Events.objects.filter(batch=batch)
    confirmed_sessions = []
    for event in events:
        confirmed_sessions_per_event = LeanerConfirmedSlots.objects.filter(
            event__id=event.id, is_coach_joined="true")
        confirmed_sessions_per_event = LearnerSerializerInDepthSerializer(
            confirmed_sessions_per_event, many=True)
        confirmed_sessions += [*confirmed_sessions_per_event.data]
    serializer = EventDepthOneSerializer(events, many=True)
    return Response({'events': serializer.data, 'confirmedSessions': confirmed_sessions}, status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
def editEvents(request, event_id):
    today = date.today()
    price_arr = addCoachPrice(request.data['coach_pricing'])
    event = Events.objects.get(id=event_id)
    expire_check = event.is_expired
    if datetime.strptime(request.data["expire_date"], "%Y-%m-%d") >= datetime.strptime(str(today), "%Y-%m-%d"):
        expire_check = False
    event_data = {
        "name": request.data["name"],
        "start_date": request.data["start_date"],
        "end_date": request.data["end_date"],
        "expire_date": request.data["expire_date"],
        "count": request.data["count"],
        "min_count": request.data["count"],
        "batch": request.data["batch"],
        "link": event.link,
        "_id": event._id,
        "coach": request.data["coach"],
        "is_expired": expire_check,
        "coach_price": price_arr
    }
    serializer = EventSerializer(instance=event, data=event_data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response({"status": "400 Bad request", "reason": "Wrong data sent"}, status=400)
    return Response({"status": "success", "data": serializer.data}, status=200)


@api_view(["DELETE"])
@permission_classes([AllowAny])
def deleteEvents(request, event_id):
    event = Events.objects.get(id=event_id)
    coach_id = []
    for coach in event.coach.all():
        coach_id.append(coach.id)
    new_event = {
        "name": event.name,
        "start_date": event.start_date,
        "batch": event.batch,
        "end_date": event.end_date,
        "expire_date": event.expire_date,
        "count": event.count,
        "min_count": event.min_count,
        "link": event.link,
        "_id": event._id,
        "coach": coach_id,
        "is_delete": True,
        "is_expired": True
    }
    serializer = EventSerializer(instance=event, data=new_event)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response({"status": "400 Bad request", "reason": "something went wrong"}, status=400)
    return Response({"status": "success, Data deleted"}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getSlotsByEventID(request, event_id):
    event = Events.objects.get(_id=event_id)
    if event.is_delete == True:
        return Response({"status": "404 not found", "reason": "data not found"}, status=404)
    else:

        all_slots = []
        for coach in event.coach.all():
            slots = ConfirmedSlotsbyCoach.objects.filter(coach_id=coach.id)
            for slot in slots:
                if slot.is_confirmed == False & slot.is_realeased == False:
                    all_slots.append(slot)
        serializer = ConfirmedSlotsbyCoachSerializer(all_slots, many=True)
        eventserializer = EventSerializer(event)
        return Response({"status": "success", "slots": serializer.data, "event": eventserializer.data}, status=200)


def createIcs(start_time, end_time, meet_link):
    fp = open("event.ics", "w")
    fp.write(
        "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//hacksw/handcal//NONSGML v1.0//EN\nBEGIN:VEVENT\nUID:uid1@example.com\nORGANIZER;CN=Meeraq:MAILTO:info@meeraq.com\nDTSTART:"
        + start_time
        + "\nDTEND:"
        + end_time
        + "\nSUMMARY:Meeraq | Coaching Session\nLOCATION:"
        + meet_link
        + "\nGEO:48.85299;2.36885\nEND:VEVENT\nEND:VCALENDAR"
    )
    fp.close()


@api_view(["POST"])
@permission_classes([AllowAny])
def confirmSlotsByLearner(request, slot_id):
    event = Events.objects.get(_id=request.data["event"])
    learners = Learner.objects.filter(
        batch=event.batch, email=request.data["email"])
    # learnerCourse = Learner.objects.get(
    #     email=request.data["email"], batch=event.batch)
    # whether learner exist in a batch or not
    if len(learners) == 0:
        return Response({"status": "Error", "reason": "user may have entered different email"}, status=405)
    else:
        coach_slot = ConfirmedSlotsbyCoach.objects.get(id=slot_id)
        coach_slot_serializer = ConfirmedSlotsbyCoachSerializer(coach_slot)
        if coach_slot.is_confirmed == False:
            coach_data = Coach.objects.get(id=coach_slot.coach_id)
            booked_slot_coach = {
                **coach_slot_serializer.data, "is_confirmed": True}
            coach_serilizer = ConfirmedSlotsbyCoachSerializer(
                instance=coach_slot, data=booked_slot_coach)
            event = Events.objects.get(_id=request.data["event"])
            Booked_slot = {
                "name": request.data["name"],
                "email": request.data["email"],
                "organisation": request.data["organisation"],
                "about": request.data['about'],
                "phone_no": request.data["phone_no"],
                "slot": coach_slot.id,
                "event": event.id,
            }
            count = int(event.count)
            coach_ids = []
            for coach in event.coach.all():
                coach_ids.append(coach.id)
            new_count = count - 1
            new_event_data = {
                "name": event.name,
                "start_date": event.start_date,
                "end_date": event.end_date,
                "expire_date": event.expire_date,
                "count": str(new_count),
                "min_count": event.min_count,
                "link": event.link,
                "_id": event._id,
                "coach": coach_ids,
            }
            event_serializer = EventSerializer(
                instance=event, data=new_event_data)
            serializer = ConfirmedSlotsbyLearnerSerializer(data=Booked_slot)
            if serializer.is_valid():
                booked_slots = LeanerConfirmedSlots.objects.all()
                deletedSlots = DeleteConfirmedSlotsbyAdmin.objects.filter(
                    event=event, email=request.data['email'])
                if request.data["warning"] == True:  # always true from frontend
                    if not bool(booked_slots) and not bool(deletedSlots):
                        serializer.save()
                    else:
                        for slot in booked_slots:
                            if (slot.email.lower() == request.data["email"].lower()) and (event.id == slot.event.id):
                                return Response({"status": "409 Bad request", "reason": "email already exist"}, status=409)
                        slotToSave = {}
                        if len(deletedSlots) == 0:
                            slotToSave = {**serializer.data,
                                          "is_reschedule": False}
                        else:
                            slotToSave = {**serializer.data,
                                          "is_reschedule": True}

                        learner_confirmed_slot_serializer = ConfirmedSlotsbyLearnerSerializer(
                            data=slotToSave)
                        if event_serializer.is_valid() and learner_confirmed_slot_serializer.is_valid():
                            event_serializer.save()
                            learner_confirmed_slot_instance = learner_confirmed_slot_serializer.save()
                            # updating rescehduled slot in deleted slots
                            for slot in deletedSlots:
                                slot_serializer = DeletedConfirmedSlotsSerializer(
                                    slot)
                                new_slot_details = {
                                    **slot_serializer.data, "rescheduled_slot": learner_confirmed_slot_instance.id}
                                new_slot_serializer = DeletedConfirmedSlotsSerializer(
                                    instance=slot, data=new_slot_details)
                                if new_slot_serializer.is_valid():
                                    new_slot_serializer.save()
                        else:
                            print("----", learner_confirmed_slot_serializer.data)
                            print(learner_confirmed_slot_serializer.errors)
                            return Response({"status": "400 bad request", "reason": "Failed to book the slot"}, status=400)
            else:
                print(serializer.errors)
                return Response({"status": "400 Bad request", "reason": "wrong data sent"}, status=400)

            if event_serializer.is_valid():
                event_serializer.save()
            else:
                print(event_serializer.errors)
            if coach_serilizer.is_valid():
                coach_serilizer.save()
            else:
                return Response({"status": "400 Bad request", "reason": "coach data is wrong"}, status=400)

            #  code to send mail
            start_time = datetime.fromtimestamp(
                (int(coach_slot.start_time) / 1000))  # converting timestamp to date
            start = (
                (start_time.replace(microsecond=0).astimezone(
                    utc).replace(tzinfo=None).isoformat() + "Z")
                .replace(":", "")
                .replace("-", "")
            )
            end_time = datetime.fromtimestamp(
                (int(coach_slot.end_time) / 1000))
            end = (
                (end_time.replace(microsecond=0).astimezone(
                    utc).replace(tzinfo=None).isoformat() + "Z")
                .replace(":", "")
                .replace("-", "")
            )

            date = datetime.fromtimestamp(
                (int(coach_slot.start_time) / 1000) + 19800).strftime("%d %B %Y")

            start_time_for_mail = datetime.fromtimestamp(
                (int(coach_slot.start_time) / 1000) + 19800)

            email_message_learner = render_to_string(
                "addevent.html",
                {"name": request.data["name"], "time": start_time_for_mail,
                    "duration": "30 Min", "date": date, "link": coach_data.meet_link},
            )
            meet_link = coach_data.meet_link
            createIcs(start, end, meet_link)
            email = EmailMessage(
                "Meeraq | Coaching Session",
                email_message_learner,
                "info@meeraq.com",  # from email address
                [request.data["email"]],  # to email address
                # [coach_data.email],  # bcc email address
                # headers={"Cc": ["info@meeraq.com"]}  # setting cc email address
            )
            email.content_subtype = "html"
            email.attach_file("event.ics", "text/calendar")
            email.send()

            if os.path.exists("event.ics"):
                os.remove("event.ics")
            else:
                print("file not found")

            # Mail_to_Coach
            coach_module_link = env("coach_url")
            email_message_coach = render_to_string(
                "coachmail.html",
                {"name": coach_data.first_name, "time": start_time_for_mail,
                    "duration": "30 Min", "date": date, "link": coach_module_link, "participant_name": request.data['name'], "course": "helllo"})
            createIcs(start, end, coach_module_link)
            email_for_coach = EmailMessage(
                "Meeraq | Coaching Session",
                email_message_coach,
                "info@meeraq.com",  # from email address
                [coach_data.email],  # to email address
                # [coach_data.email],  # bcc email address
                # headers={"Cc": ["info@meeraq.com"]}  # setting cc email address
            )
            email_for_coach.content_subtype = "html"
            email_for_coach.attach_file("event.ics", "text/calendar")
            email_for_coach.send()

            if os.path.exists("event.ics"):
                os.remove("event.ics")
            else:
                print("file not found")
            #  code to send mail ends here
            return Response({"status": "success", "data": serializer.data}, status=200)
        else:
            return Response({"status": "Error", "reason": "Slot is already Booked"}, status=408)


@api_view(["GET"])
@permission_classes([AllowAny])
def getConfirmSlotsByLearner(request):
    booked_slots = LeanerConfirmedSlots.objects.all()
    serializer = ConfirmedLearnerSerializer(booked_slots, many=True)
    return Response({"status": "success", "data": serializer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getConfirmSlotsByLearnerByEventId(request, event_id):
    booked_slots = LeanerConfirmedSlots.objects.filter(event=event_id)
    serializer = ConfirmedLearnerSerializer(booked_slots, many=True)
    return Response({"status": "success", "data": serializer.data}, status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
def editConfirmSlotsByLearnerBySlotId(request, slot_id):
    booked_slots = LeanerConfirmedSlots.objects.get(id=slot_id)
    newSlot = {
        "name": booked_slots.name,
        "status": request.data['status'],
        "email": booked_slots.email,
        "phone_no": booked_slots.phone_no,
        "organisation": booked_slots.organisation,
        "event": booked_slots.event.id,
        "slot": booked_slots.slot.id
    }
    serializer = ConfirmedSlotsbyLearnerSerializer(
        instance=booked_slots, data=newSlot)

    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data}, status=200)
    else:
        return Response({"message": "Invalid data"}, status=400)


def createCancledIcs(start_time, end_time):
    fp = open("cancelevent.ics", "w")
    fp.write(
        "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//hacksw/handcal//NONSGML v1.0//EN\nBEGIN:VEVENT\nUID:uid1@example.com\nORGANIZER;CN=Meeraq:MAILTO:info@meeraq.com\nDTSTART:"
        + start_time
        + "\nDTEND:"
        + end_time
        + "\nSUMMARY:Meeraq |Canceled Coaching Session"
        + "\nGEO:48.85299;2.36885\nEND:VEVENT\nEND:VCALENDAR"
    )
    fp.close()


@api_view(["DELETE"])
@permission_classes([AllowAny])
def deleteConfirmSlotsAdmin(request, slot_id):
    booked_slots = LeanerConfirmedSlots.objects.get(id=slot_id)

    start_time = datetime.fromtimestamp(
        (int(booked_slots.slot.start_time) / 1000))  # converting timestamp to date
    start = (
        (start_time.replace(microsecond=0).astimezone(
            utc).replace(tzinfo=None).isoformat() + "Z")
        .replace(":", "")
        .replace("-", "")
    )
    end_time = datetime.fromtimestamp((int(booked_slots.slot.end_time) / 1000))
    end = (
        (end_time.replace(microsecond=0).astimezone(
            utc).replace(tzinfo=None).isoformat() + "Z")
        .replace(":", "")
        .replace("-", "")
    )

    date = datetime.fromtimestamp(
        (int(booked_slots.slot.start_time) / 1000) + 19800).strftime("%d %B %Y")
    start_time_for_mail = datetime.fromtimestamp(
        (int(booked_slots.slot.start_time) / 1000) + 19800)
    email_message_learner = render_to_string(
        "cancelEvent.html",
        {"time": start_time_for_mail,
         "date": date},
    )

    createCancledIcs(start, end)
    coach = Coach.objects.get(id=booked_slots.slot.coach_id)
    email = EmailMessage(
        "Meeraq | Canceled Coaching Session",
        email_message_learner,
        "info@meeraq.com",
        [booked_slots.email, coach.email],
    )
    email.content_subtype = "html"
    email.attach_file("cancelevent.ics", "text/calendar")
    email.send()
    if os.path.exists("cancelevent.ics"):
        os.remove("cancelevent.ics")
    else:
        print("file not found")

    booked_slots.delete()

    new_booked_slots = LeanerConfirmedSlots.objects.all()
    serializer = ConfirmedSlotsbyLearnerSerializer(new_booked_slots, many=True)
    return Response({"status": "success", "data": serializer.data}, status=200)

    # ...............


@api_view(["POST"])
@permission_classes([AllowAny])
def DeletedConfirmedSlots(request, slot_id):
    deleted_slots = LeanerConfirmedSlots.objects.get(
        id=slot_id)  # slot which needs to be deleted
    delSlot = {
        "batch_name": deleted_slots.event.batch,
        "requested_person": request.data['requested_person'],
        "reason": request.data['delete_reason'],
        "admin_name": request.data['admin_name'],
        "name": deleted_slots.name,
        "email": deleted_slots.email,
        "phone_no": deleted_slots.phone_no,
        "slot_id": deleted_slots.slot.id,
        "event": deleted_slots.event.id,
        "organisation": deleted_slots.organisation
    }
    serializer = DeletedConfirmedSlotsSerializer(data=delSlot)
    if serializer.is_valid():
        serializer.save()
        if request.data['requested_person'] == "participant":
            coach_slot_serializer = ConfirmedSlotsbyCoachSerializer(
                deleted_slots.slot)
            coach_slot_update_details = {
                **coach_slot_serializer.data, "is_confirmed": False}
            coach_updated_slot_serializer = ConfirmedSlotsbyCoachSerializer(
                instance=deleted_slots.slot, data=coach_slot_update_details)
            if coach_updated_slot_serializer.is_valid():
                coach_updated_slot_serializer.save()
            else:
                print("Error making slot available")
        start_time = datetime.fromtimestamp(
            (int(deleted_slots.slot.start_time) / 1000))  # converting timestamp to date
        start = ((start_time.replace(microsecond=0).astimezone(utc).replace(
            tzinfo=None).isoformat() + "Z").replace(":", "").replace("-", ""))
        end_time = datetime.fromtimestamp(
            (int(deleted_slots.slot.end_time) / 1000))
        end = ((end_time.replace(microsecond=0).astimezone(utc).replace(
            tzinfo=None).isoformat() + "Z").replace(":", "").replace("-", ""))
        date = datetime.fromtimestamp(
            (int(deleted_slots.slot.start_time) / 1000) + 19800).strftime("%d %B %Y")
        start_time_for_mail = datetime.fromtimestamp(
            (int(deleted_slots.slot.start_time) / 1000) + 19800)
        email_message_learner = render_to_string(
            "cancelEvent.html", {"time": start_time_for_mail, "date": date})
        createCancledIcs(start, end)
        coach = Coach.objects.get(id=deleted_slots.slot.coach_id)
        email = EmailMessage("Meeraq | Canceled Coaching Session", email_message_learner,
                             "info@meeraq.com", [deleted_slots.email, coach.email])
        email.content_subtype = "html"
        email.attach_file("cancelevent.ics", "text/calendar")
        email.send()
        if os.path.exists("cancelevent.ics"):
            os.remove("cancelevent.ics")
        else:
            print("file not found")
        deleted_slots.delete()
        return Response({"status": "success"}, status=201)
    else:
        print(serializer.errors)
        return Response({"status": "Bad Request"}, status=400)
     # ...........


@api_view(["GET"])
@permission_classes([AllowAny])
def DeletedConfirmSlots(request, confirmed_slot_id):
    deleted_slots = DeleteConfirmedSlotsbyAdmin.objects.filter(
        rescheduled_slot=confirmed_slot_id)
    serializer = GetNestedDeletedConfirmedSlotsSerializer(
        deleted_slots, many=True)
    return Response({"status": "success", "data": serializer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def DeletedSession(request):
    deleted_session = DeleteConfirmedSlotsbyAdmin.objects.all()
    serializer = GetNestedDeletedConfirmedSlotsSerializer(
        deleted_session, many=True)
    return Response({"status": "success", "data": serializer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getLearnerConfirmedSlotsByCoachId(request, coach_id):
    booked_slots = LeanerConfirmedSlots.objects.filter(slot__coach_id=coach_id)
    serializer = ConfirmedLearnerSerializer(booked_slots, many=True)
    return Response({"status": "success", "data": serializer.data}, status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
def learnerDataUpload(request):
    batches = set()
    for learner in request.data['participent']:
        is_exist = Learner.objects.filter(
            unique_check=learner['batch']+"|"+learner['email'])
        if len(is_exist) > 0:
            continue
        else:
            if 'phone' in learner.keys():
                learner_data = Learner(first_name=learner['first_name'], last_name=learner['last_name'], email=learner['email'],
                                       batch=learner['batch'], phone=learner['phone'], unique_check=learner['batch']+"|" + learner['email'], course=learner['course'])
            else:
                learner_data = Learner(first_name=learner['first_name'], last_name=learner['last_name'], email=learner['email'],
                                       batch=learner['batch'], unique_check=learner['batch']+"|" + learner['email'], course=learner['course'])
            learner_data.save()
            is_batch_exist = Batch.objects.filter(batch=learner['batch'])
            if not is_batch_exist:
                batch_data = Batch(
                    batch=learner['batch'], start_date=learner['start_date'], end_date=learner['end_date'])
                batch_data.save()
    #             batches.add(
    #                 {'name': learner['batch'], 'start_date': learner['start_date'], 'end_date': learner['end_date']})
    # for batch in batches:
    #     batch_data = Batch(batch=batch)
    #     batch_data.save()
    return Response({"status": "success"}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getLearnerBatchwise(request, batch_id):
    learners = Learner.objects.filter(batch=batch_id)
    serilizer = LearnerDataUploadSerializer(learners, many=True)
    return Response({"status": "success", "data": serilizer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getBatches(request):
    batches = Batch.objects.all()
    serilizer = BatchSerializer(batches, many=True)
    return Response({"status": "success", "data": serilizer.data}, status=200)


def generateManagementToken():
    expires = 24 * 3600
    now = datetime.utcnow()
    exp = now + timedelta(seconds=expires)
    return jwt.encode(payload={
        'access_key': env('100MS_APP_ACCESS_KEY'),
        'type': 'management',
        'version': 2,
        'jti': str(uuid.uuid4()),
        'iat': now,
        'exp': exp,
        'nbf': now
    }, key=env('100MS_APP_SECRET'))


@api_view(["GET"])
@permission_classes([AllowAny])
def getManagementToken(request):
    management_token = generateManagementToken()
    return Response({"message": "Success", "management_token": management_token}, status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
def getCurrentBookedSlot(request):
    learner_email = request.data['learner_email']
    meet_link = env("coach_url")+"join-session/" + request.data['room_id']
    current_time = request.data['time']
    print(meet_link, current_time)
    today_date = datetime.date(datetime.today())
    try:
        coach = Coach.objects.get(meet_link=meet_link)
        try:
            booked_slot = LeanerConfirmedSlots.objects.get(
                slot__coach_id=coach.id, email=learner_email, slot__date=today_date)
            if booked_slot and (current_time > (int(booked_slot.slot.start_time) - 300000)) and (current_time < int(booked_slot.slot.end_time)):
                newSlot = {
                    "name": booked_slot.name,
                    "status": booked_slot.status,
                    "email": booked_slot.email,
                    "phone_no": booked_slot.phone_no,
                    "organisation": booked_slot.organisation,
                    "event": booked_slot.event.id,
                    "slot": booked_slot.slot.id,
                    "is_learner_joined": "true"
                }
                booked_slot_serializer = ConfirmedSlotsbyLearnerSerializer(
                    instance=booked_slot, data=newSlot)
                if booked_slot_serializer.is_valid():
                    booked_slot_serializer.save()
                else:
                    print(booked_slot_serializer.errors)
                new_booked_slot = LeanerConfirmedSlots.objects.get(
                    slot__coach_id=coach.id, email=learner_email, slot__date=today_date)
                new_booked_slot_serializer = ConfirmedLearnerSerializer(
                    new_booked_slot)
                return Response({"message": "Success", "data": new_booked_slot_serializer.data}, status=200)
            else:
                return Response({"No session found"}, status=401)
        except:
            return Response({"message": "No session found"}, status=401)
    except:
        print("Error")
        return Response({"message": "Invalid Link"}, status=400)


@api_view(["GET"])
@permission_classes([AllowAny])
def getServiceApprovalData(request):
    data = ServiceApproval.objects.all()
    serializer = ServiceApprovalDepthOneSerializer(data, many=True)
    return Response({"status": "success", "data": serializer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getServiceApprovalDatabyrefId(request, ref_id):
    data = ServiceApprovalData.objects.get(ref_id=ref_id)
    serializer = ServiceApprovalSerializer(data)
    return Response({"status": "success", "data": serializer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getServiceApprovalDatabyCoachID(request, coach_id):
    data = ServiceApproval.objects.filter(coach=coach_id)
    serializer = ServiceApprovalDepthOneSerializer(data, many=True)
    return Response({"status": "success", "data": serializer.data}, status=200)


# def addServiceApprovalEntries(entries):
#     serivce_approval_entries_ids = []
#     for item in entries:
#         try:
#             service_approval_entry = ServiceApprovalEntry.objects.get(
#                 no_of_sessions=item['no_of_sessions'], price=item['price'])
#             serivce_approval_entries_ids.append(service_approval_entry.id)
#         except:
#             new_data = ServiceApprovalEntrySerializer(data=item)
#             if new_data.is_valid():
#                 instance = new_data.save()
#                 serivce_approval_entries_ids.append(instance.id)
#     print(serivce_approval_entries_ids)
#     return serivce_approval_entries_ids


@api_view(["POST"])
@permission_classes([AllowAny])
def addServiceApprovalData(request):
    today = date.today()
    service_approval_entries = addServiceApprovalEntries(
        request.data['entries'])
    service_approval_data = {
        'po_id': request.data['po_id'],
        'batch': request.data['batch'],
        'entries': service_approval_entries,
        'coach': request.data['coach'],
        'generated_on': today,
        'ref_id': "2",
        'responded_on': None
    }
    serializer = ServiceApprovalSerializer(data=service_approval_data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success"}, status=201)
    else:
        print(serializer.errors)
        return Response({"status": "Bad Request"}, status=400)
    # month = [
    #     "january",
    #     "february",
    #     "march",
    #     "april",
    #     "may",
    #     "june",
    #     "july",
    #     "august",
    #     "september",
    #     "october",
    #     "november",
    #     "december",
    # ]
    # reference = str(request.data['coach_id']) + '-' + str(today) + \
    #     "-" + str((month.index(request.data['generate_for_month'])+1)*10)
    # service_data = {
    #     "ref_id": reference,
    #     "fees": request.data['fees'],
    #     "total_no_of_sessions": request.data['total_no_of_sessions'],
    #     "generated_date": today,
    #     "generate_for_month": request.data['generate_for_month'],
    #     "generate_for_year": request.data['generate_for_year'],
    #     "batch": request.data['batch'],
    #     "coach_id": request.data['coach_id']
    # }
    # serializer = ServiceApprovalSerializer(data=service_data)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response({"status": "success"}, status=201)
    # else:
    #     return Response({"status": "Bad Request"}, status=400)


# @api_view(["POST"])
# @permission_classes([AllowAny])
# def approveByFinance(request):
#     today = date.today()
#     ref_id = request.data['ref_id']
#     service_request = ServiceApprovalData.objects.get(
#         ref_id=ref_id)
#     if request.data['is_approved'] == "true":
#         service_data = {
#             "ref_id": ref_id,
#             "fees": service_request.fees,
#             "total_no_of_sessions": service_request.total_no_of_sessions,
#             "generated_date": service_request.generated_date,
#             "generate_for_month": service_request.generate_for_month,
#             "generate_for_year": service_request.generate_for_year,
#             "coach_id": service_request.coach_id.id,
#             "is_approved": "true",
#             "invoice_no": request.data['invoice_no'],
#             "response_by_finance_date": today
#         }
#     else:
#         service_data = {
#             "ref_id": ref_id,
#             "fees": service_request.fees,
#             "total_no_of_sessions": service_request.total_no_of_sessions,
#             "generated_date": service_request.generated_date,
#             "generate_for_month": service_request.generate_for_month,
#             "generate_for_year": service_request.generate_for_year,
#             "coach_id": service_request.coach_id.id,
#             "is_approved": "false",
#             "invoice_no": request.data['invoice_no'],
#             "response_by_finance_date": today,
#             "rejection_reason": request.data['rejection_reason']
#         }

#     serializer = ServiceApprovalSerializer(
#         instance=service_request, data=service_data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({"status": "success"}, status=201)
#     else:
#         print(serializer.errors)
#         return Response({"status": "Bad Request"}, status=400)


@api_view(["POST"])
@permission_classes([AllowAny])
def updateServiceApprovalStatus(request, service_approval_id):
    today = date.today()
    service_approval = ServiceApproval.objects.get(id=service_approval_id)
    if request.data['status'] == True:
        service_approval.is_approved = True
    else:
        service_approval.is_approved = False
    service_approval.responded_on = today
    service_approval.save()
    return Response(status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
def registerFinanceUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        newUser = User.objects.create_user(
            username=request.data["email"], email=request.data["email"], password=request.data["password"]
        )
        newUser.save()
    else:
        return Response(status="403")
    user = User.objects.get(username=serializer.data["email"])
    userToSave = User.objects.get(username=serializer.data["email"])
    newProfile = Profile(user=userToSave, type="finance",
                         email=serializer.data["email"])
    newProfile.save()
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"status": 200, "payload": serializer.data, "token": str(token)})


@api_view(["GET"])
@permission_classes([AllowAny])
def exportLearnerConfirmedSlotsByEventId(request, event_id):
    confirmed_slot_file = LearnerConfirmedSlotsResource()
    dataset = confirmed_slot_file.export(
        LeanerConfirmedSlots.objects.filter(event=event_id))
    response = HttpResponse(
        dataset.xls, content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = 'attachment; filename="confirmed slots.xls"'
    return response


@api_view(["POST"])
@permission_classes([AllowAny])
def confirmCoachJoined(request, slot_id):
    booked_slots = LeanerConfirmedSlots.objects.get(id=slot_id)
    newSlot = {
        "name": booked_slots.name,
        "status": booked_slots.status,
        "email": booked_slots.email,
        "phone_no": booked_slots.phone_no,
        "organisation": booked_slots.organisation,
        "event": booked_slots.event.id,
        "slot": booked_slots.slot.id,
        "is_coach_joined": "true"
    }
    serializer = ConfirmedSlotsbyLearnerSerializer(
        instance=booked_slots, data=newSlot)

    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data}, status=200)
    else:
        return Response({"messgae": "Invalid data"}, status=400)


@api_view(["POST"])
@permission_classes([AllowAny])
def getSlotByMonth(request):
    slots = LeanerConfirmedSlots.objects.filter(
        is_coach_joined="true", slot__coach_id=request.data['coach'])
    month_slot = []
    for slot in slots.all():
        if slot.slot.date.strftime("%m-%Y") == request.data['date']:
            serializer = ConfirmedLearnerSerializer(slot)
            month_slot.append(serializer.data)
    return Response({"message": "success", "data": month_slot}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getSlotByBatchAndCoach(request, batch, coach_id):
    batch = Batch.objects.get(batch=batch)
    events = Events.objects.filter(batch=batch.batch)
    all_slots = []
    for event in events:
        confirmed_slots = LeanerConfirmedSlots.objects.filter(
            event=event.id, is_coach_joined="true", slot__coach_id=coach_id)
        confirmed_slots_serializer = LearnerSerializerInDepthSerializer(
            confirmed_slots, many=True)
        all_slots = all_slots + [*confirmed_slots_serializer.data]
    return Response({"message": "success", "confirmed_slots": all_slots}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getBatchesOfCoach(request, coach_id):
    today = date.today()
    batchesNames = set()
    events = Events.objects.filter(coach__id=coach_id)
    for event in events:
        batchesNames.add(event.batch)
    batches_completed = []
    for batch in batchesNames:
        batch_queryset = Batch.objects.get(batch=batch)
        if batch_queryset.end_date and batch_queryset.end_date < today:
            batches_completed.append(batch_queryset.batch)
    print(batches_completed)
    return Response({"batches": batches_completed}, status=200)


# post api for PO
@api_view(["POST"])
@permission_classes([AllowAny])
def createPurchaseOrder(request):
    # checking whether po numbers are unique or not
    print(request.data)
    existing_po_list = PurchaseOrder.objects.filter(
        po_no=request.data['po_no'])
    if len(existing_po_list) > 0:
        return Response({"status": "Duplicate PO number"}, status=401)
    po = {
        'po_no': request.data['po_no'],
        'rate': 500,
        'number_of_session': request.data['number_of_session'],
        'coach': request.data['coach'],
        'valid_till': request.data['valid_till']
    }
    serializer = PurchaseOrderSerializer(data=po)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success"}, status=200)
    else:
        print(serializer.errors)
        return Response({"message": "Invalid data"}, status=400)


@api_view(["POST"])
@permission_classes([AllowAny])
def editPurchaseOrder(request, po_id):
    # checking whether po numbers are unique or not
    po = PurchaseOrder.objects.get(id=po_id)
    coach = Coach.objects.get(id=request.data['coach'])
    existing_po_list = PurchaseOrder.objects.filter(
        po_no=request.data['po_no']).exclude(id=po_id)
    if len(existing_po_list) > 0:
        return Response({"status": "Duplicate PO number"}, status=401)
    po.number_of_session = request.data['number_of_session']
    po.coach = coach
    po.valid_till = request.data['valid_till']
    po.po_no = request.data['po_no']
    po.save()
    return Response({"status": "success"}, status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
def updatePurchaseOrderStatus(request, po_id):
    # checking whether po numbers are unique or not
    po = PurchaseOrder.objects.get(id=po_id)
    print(po)
    if request.data['status'] == 'OPEN' or request.data['status'] == 'CLOSED':
        po.status = request.data['status']
        po.save()
    else:
        return Response({"status": "Duplicate PO number"}, status=401)
    return Response({"status": "success"}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getpurchaseOrder(request):
    po = PurchaseOrder.objects.all()
    today = date.today()
    for po_item in po:
        if today > po_item.valid_till:
            po_item.status = "CLOSED"
            po_item.save()
    updated_po = PurchaseOrder.objects.all()
    serializer = PurchaseOrderDepthOneSerializer(updated_po, many=True)
    return Response({"status": "success", "data": serializer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getUninvoicedLearnerConfirmedSlotOfCoach(request, coach_id):
    slots = LeanerConfirmedSlots.objects.filter(
        slot__coach_id=coach_id, service_approval=None, is_coach_joined="true")
    serializer = LearnerSerializerInDepthSerializer(slots, many=True)
    return Response({"status": "success", "data": serializer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getLearnerConfirmedSlotsByServiceApproval(request, id):
    booked_slots = LeanerConfirmedSlots.objects.filter(
        service_approval__id=id)
    serializer = ConfirmedLearnerSerializer(booked_slots, many=True)
    return Response({"status": "success", "data": serializer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getPurchaseOrderofCoachByStatus(request, status, coach_id):
    po = PurchaseOrder.objects.filter(coach=coach_id, status=status)
    today = date.today()
    if status == "OPEN":
        for po_item in po:
            if today > po_item.valid_till:
                po_item.status = "CLOSED"
                po_item.save()
        open_po = PurchaseOrder.objects.filter(coach=coach_id, status="OPEN")
        open_po_serializer = PurchaseOrderDepthOneSerializer(
            open_po, many=True)
        return Response({"status": "success", "data": open_po_serializer.data}, status=200)
    serializer = PurchaseOrderDepthOneSerializer(po, many=True)
    return Response({"status": "success", "data": serializer.data}, status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
def createServiceApproval(request):
    po = PurchaseOrder.objects.get(po_no=request.data['po_no'])
    approval = {
        'invoice_number': request.data['invoice_number'],
        'po': po.id,
        'number_of_session': request.data['number_of_session'],
        'is_approved': False,
        'payment_date': None,
        'response_date': None
    }
    serializer = ServiceApprovalSerializer(data=approval)
    if serializer.is_valid():
        service_approval = serializer.save()
        # updating no. of sessions consumed
        po.number_of_session_consumed = po.number_of_session_consumed + \
            int(request.data['number_of_session'])
        po.save()
        # adding service approval in learner confirmed slot
        slot_ids = request.data['slot_ids']
        for i in range(int(request.data['number_of_session'])):
            slot = LeanerConfirmedSlots.objects.get(id=slot_ids[i])
            slot.service_approval = service_approval
            slot.save()
        return Response({"status": "success", "data": serializer.data}, status=200)
    else:
        return Response({"message": str(serializer.errors)}, status=400)


@api_view(["POST"])
@permission_classes([AllowAny])
def editServiceapproval(request, id):
    service_approval = ServiceApproval.objects.get(id=id)
    purchase_order = PurchaseOrder.objects.get(id=service_approval.po.id)

    # updating servical approval in learner confirmed slot
    if int(request.data['number_of_session']) > service_approval.number_of_session:
        for i in range(int(request.data['number_of_session']) - service_approval.number_of_session):
            slot = LeanerConfirmedSlots.objects.get(
                id=request.data['slot_ids'][i])
            slot.service_approval = service_approval
            slot.save()
    if int(request.data['number_of_session']) < service_approval.number_of_session:
        for i in range(service_approval.number_of_session - int(request.data['number_of_session'])):
            slot = LeanerConfirmedSlots.objects.get(
                id=request.data['invoiced_slot_ids'][i])
            slot.service_approval = None
            slot.save()

    # updating number of consumed session in po
    purchase_order.number_of_session_consumed = purchase_order.number_of_session_consumed - \
        service_approval.number_of_session + \
        int(request.data['number_of_session'])
    # ----------
    service_approval.number_of_session = request.data['number_of_session']
    service_approval.invoice_number = request.data['invoice_number']
    service_approval.response_date = None
    service_approval.is_approved = False
    purchase_order.save()
    service_approval.save()
    return Response({}, status=200)
    # serializer = ServiceApprovalSerializer(service)
    # approval = {
    #     **serializer.data,
    #     'invoice_no.': request.data['invoice no.'],
    #     'number_of_session': request.data['number_of_session']
    # }
    # serializerTwo = ServiceApprovalSerializer(instance=service, data=approval)
    # if serializerTwo.is_valid():
    #     serializerTwo.save()
    #     return Response({"status": "success", "data": serializerTwo.data}, status=200)
    # else:
    #     return Response({"message": str(serializerTwo.errors)}, status=400)


@api_view(["GET"])
@permission_classes([AllowAny])
def getServiceApproval(request):
    approval = ServiceApproval.objects.all()
    serializer = ServiceApprovalSerializer(approval, many=True)
    return Response({"status": "success", "data": serializer.data}, status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
def rejectServiceApproval(request, id):
    serviceApproval = ServiceApproval.objects.get(id=id)
    today = datetime.now()
    today_date = date.today()
    rejection = {
        'reason': request.data['rejection_reason'],
        'date': today
    }
    serializer = RejectedSerializer(data=rejection)
    if serializer.is_valid():
        rejected = serializer.save()
        serviceApproval.rejected.add(rejected.id)
        if serviceApproval.is_approved == True:
            po = PurchaseOrder.objects.get(id=serviceApproval.po.id)
            if today_date < po.valid_till:
                po.status = "OPEN"
            po.number_of_session_approved = po.number_of_session_approved - \
                serviceApproval.number_of_session
            po.save()
        serviceApproval.response_date = today
        serviceApproval.is_approved = False
        serviceApproval.save()
        return Response({"status": "success", "data": serializer.data}, status=200)
    else:
        print(serializer.errors)
        return Response({"message": str(serializer.errors)}, status=400)


@api_view(["POST"])
@permission_classes([AllowAny])
def approveServiceApproval(request, id):
    service_approval = ServiceApproval.objects.get(id=id)
    po = PurchaseOrder.objects.get(id=service_approval.po.id)
    today = date.today()
    if service_approval.is_approved == True:
        # service approval is already approved
        return Response({}, status=201)
    service_approval.is_approved = True
    service_approval.response_date = today
    # updating PO status if all sessions are consumed
    if po.number_of_session == po.number_of_session_approved + service_approval.number_of_session:
        po.status = "CLOSED"
        # updating number of sessions approved in PO
    po.number_of_session_approved = po.number_of_session_approved + \
        service_approval.number_of_session
    po.save()
    service_approval.save()
    return Response({}, status=201)


@api_view(["POST"])
@permission_classes([AllowAny])
def updateSessionAttendance(request, slot_id):
    print(request.data, slot_id)
    slot = LeanerConfirmedSlots.objects.get(id=slot_id)
    slot.is_coach_joined = request.data['coach']
    slot.is_learner_joined = request.data['learner']
    slot.save()
    return Response({}, status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
def approveServiceApprovalByFinance(request, id):
    service_approval = ServiceApproval.objects.get(id=id)
    date = datetime.strptime(request.data['date'], "%Y-%m-%d").date()
    service_approval.payment_date = date
    service_approval.save()
    return Response({}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getRejected(request):
    rejects = Rejected.objects.all()
    serializer = RejectedSerializer(rejects, many=True)
    return Response({"status": "success", "data": serializer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getPurchaseOrderByCoach(request, coach_id):
    po = PurchaseOrder.objects.filter(coach__id=coach_id)
    today = date.today()
    for po_item in po:
        if today > po_item.valid_till:
            po_item.status = "CLOSED"
            po_item.save()
    updated_po = PurchaseOrder.objects.filter(coach__id=coach_id)
    serializer = PurchaseOrderDepthOneSerializer(
        updated_po, many=True)  # change serilizer
    return Response({"status": "success", "data": serializer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getPurchaseOrderByStatus(request, status):
    po = PurchaseOrder.objects.filter(status=status)
    today = date.today()
    if status == "OPEN":
        for po_item in po:
            if today > po_item.valid_till:
                po_item.status = "CLOSED"
                po_item.save()
        open_po = PurchaseOrder.objects.filter(status="OPEN")
        open_po_serializer = PurchaseOrderDepthOneSerializer(
            open_po, many=True)
        return Response({"status": "success", "data": open_po_serializer.data}, status=200)

    serializer = PurchaseOrderDepthOneSerializer(
        po, many=True)
    return Response({"status": "success", "data": serializer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getServiceApprovalByPO(request, po):
    existing = ServiceApproval.objects.filter(po=po)
    serializer = ServiceApprovalSerializer(existing, many=True)
    return Response({"status": "success", "data": serializer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getServiceApprovalBycoach(request, coach_id):
    existing = ServiceApproval.objects.filter(po__coach=coach_id)
    serializer = ServiceApprovalDepthOneSerializer(existing, many=True)
    return Response({"status": "success", "data": serializer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getServiceApprovalbyType(request, type):
    if type == "APPROVED":
        service_approvals = ServiceApproval.objects.filter(is_approved=True)
    if type == "PENDING":
        service_approvals = ServiceApproval.objects.filter(
            is_approved=False, response_date=None)
    if type == "REJECTED":
        service_approvals = ServiceApproval.objects.filter(
            is_approved=False).exclude(response_date=None)
    if type == "PAID":
        service_approvals = ServiceApproval.objects.all().exclude(payment_date=None)
    if type == "PAYMENT_PENDING":
        service_approvals = ServiceApproval.objects.filter(
            is_approved=True, payment_date=None)
    serializer = ServiceApprovalDepthTwoSerializer(
        service_approvals, many=True)
    return Response({"status": "success", "service_approvals": serializer.data}, status=200)
