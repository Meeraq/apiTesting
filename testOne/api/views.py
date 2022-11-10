import email
import uuid
from django.template.loader import render_to_string
import jwt
from datetime import datetime, time, timedelta
from django.core.mail import EmailMessage
import os
from django.core.mail import send_mail
from base.resources import ConfirmedSlotResource
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
from base.models import Events,SubmitedQuestion
from base.models import LeanerConfirmedSlots
from base.models import Batch, Learner
from base.models import Competency, CourseAssesment, Question, SubCompetency
from base.models import Assesment
from base.models import Leader
from .serializers import (
    SubmitedQuestionserializer,SubmittedAssesmentserializer,AddpeopleByLeaderserializer,
    AdminReqSerializer,
    AssesmentLinkserializer,
    BatchSerializer,
    Competencyserializer,
    ConfirmedLearnerSerializer,
    ConfirmedSlotsbyCoachSerializer,
    ConfirmedSlotsbyLearnerSerializer,
    CourseAssesmentserializer,
    EditUserSerializer,
    EventSerializer,
    GetAdminReqSerializer,
    CoachSerializer,
    LeaderSerializer,
    LearnerDataUploadSerializer,
    Questionserializer,
    SlotForCoachSerializer,
    SubCompetencyserializer,
    UserSerializer,
    ProfileSerializer,
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
            "info@meeraq.com",
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
                        "meet_link": userProfile.meet_link
                    }
                )
            else:
                return Response({"reason": "No user found"}, status=404)
        elif user.profile.type == "admin":
            if request.data['type'] == 'admin':
                userProfile = User.objects.get(email=username)
                token = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        "status": "200",
                        "username": user.username,
                        "token": str(token[0]),
                        "email": userProfile.email,
                        "usertype": user.profile.type,
                        "id": userProfile.id,
                    }
                )
            else:
                return Response({"reason": "No user found"}, status=404)
        elif user.profile.type == "leader":
            if request.data['type'] == 'leader':
                userProfile = Leader.objects.get(email=username)
                token = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        "username": user.username,
                        "first_name": userProfile.first_name,
                        "middle_name": userProfile.middle_name,
                        "last_name": userProfile.last_name,
                        "token": str(token[0]),
                        "email": userProfile.email,
                        "usertype": user.profile.type,
                        "id": userProfile.id,
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




@api_view(["POST"])
@permission_classes([AllowAny])
def makeSlotRequest(request):
    adminRequest = AdminRequest(
        name=request.data["request_name"], expire_date=request.data["expiry_date"])
    adminRequest.save()
    for coach in request.data["coach_id"]:
        single_coach = Coach.objects.get(id=coach)
        email_message = render_to_string(
            "makerequest.html", {
                "expire_date": request.data["expiry_date"], "coach_name": single_coach.first_name}
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
    req = AdminRequest.objects.all()
    serilizedData = GetAdminReqSerializer(req, many=True)
    return Response({"details": "success", "Data": serilizedData.data}, status=200)


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


@api_view(["POST"])
@permission_classes([AllowAny])
def addEvent(request):
    event_id = uuid.uuid1()
    event_data = {
        "name": request.data["name"],
        "start_date": request.data["start_date"],
        "end_date": request.data["end_date"],
        "expire_date": request.data["expire_date"],
        "count": request.data["count"],
        "min_count": request.data["count"],
        "link": "https://learner.meeraq.com/book-slot/" + str(event_id) + "/",
        "_id": str(event_id),
        "coach": request.data["coach"],
        "batch": request.data["batch"]
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
    serializer = EventSerializer(updated_events, many=True)
    return Response({"status": "success", "data": serializer.data}, status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
def editEvents(request, event_id):
    today = date.today()
    event = Events.objects.get(id=event_id)
    expire_check = event.is_expired
    if datetime.strptime(request.data["expire_date"], "%Y-%m-%d") > datetime.strptime(str(today), "%Y-%m-%d"):
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
        "is_expired": expire_check
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
                if request.data["warning"] == True:
                    if not bool(booked_slots):
                        serializer.save()
                    else:
                        for slot in booked_slots:
                            if (slot.email == request.data["email"]) and (event.id == slot.event.id):
                                return Response({"status": "409 Bad request", "reason": "email already exist"}, status=409)
                            else:
                                serializer.save()
                                if event_serializer.is_valid():
                                    event_serializer.save()
                                else:
                                    print(event_serializer.errors)
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
                [coach_data.email],  # bcc email address
                # headers={"Cc": ["info@meeraq.com"]}  # setting cc email address
            )
            email.content_subtype = "html"
            email.attach_file("event.ics", "text/calendar")
            email.send()

            if os.path.exists("event.ics"):
                os.remove("event.ics")
            else:
                print("file not found")
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
        print(serializer.errors)
        return Response({"messgae": "Invalid data"}, status=400)


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
    arr_set = Batch.objects.all()
    batch_serilizer = BatchSerializer(arr_set, many=True)
    for batch in batch_serilizer.data:
        batches.add(batch['batch'])
    arr_set.delete()
    for learner in request.data['participent']:
        is_exist = Learner.objects.filter(
            unique_check=learner['batch']+"|"+learner['email'])
        if len(is_exist) > 0:
            continue
        else:
            if 'phone' in learner.keys():
                learner_data = Learner(first_name=learner['first_name'], last_name=learner['last_name'], email=learner['email'],
                                       batch=learner['batch'], phone=learner['phone'], unique_check=learner['batch']+"|" + learner['email'], course=learner['course'])
                batches.add(learner['batch'])
            else:
                learner_data = Learner(first_name=learner['first_name'], last_name=learner['last_name'], email=learner['email'],
                                       batch=learner['batch'], unique_check=learner['batch']+"|" + learner['email'], course=learner['course'])
                batches.add(learner['batch'])
            learner_data.save()
    for batch in batches:
        batch_data = Batch(batch=batch)
        batch_data.save()
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
    meet_link = "https://coach.meeraq.com/join-session/" + \
        request.data['room_id']
    current_time = request.data['time']
    today_date = datetime.date(datetime.today())
    try:
        coach = Coach.objects.get(meet_link=meet_link)
        try:
            booked_slot = LeanerConfirmedSlots.objects.get(
                slot__coach_id=coach.id, email=learner_email, slot__date=today_date)
            if booked_slot & current_time > ( booked_slot.slot__start_time - 300000) &  current_time < booked_slot.slot__end_time:
                booked_slot_serializer = ConfirmedLearnerSerializer(
                    booked_slot)
                return Response({"message": "Success", "data": booked_slot_serializer.data}, status=200)
            else:
                return Response({"No session found"}, status=401)
        except:
            return Response({"message": "No session found"}, status=401)
    except:
        return Response({"message": "Invalid Link"}, status=400)

@api_view(["POST"])
@permission_classes([AllowAny])
def addQuestions(request):
    for question in request.data:
        serilizer = Questionserializer(data=question)
        if serilizer.is_valid():
            serilizer.save()
        else:
            print(serilizer.errors)
            return Response({"status": "bad request"}, status=400)
    return Response({"status": "success"}, status=200)




@api_view(["POST"])
@permission_classes([AllowAny])
def addSubCompitency(request):
    # new_sub_competency = SubCompetency(
    #     name = request.data['name'],
    #     competency = request.data['competency'],
    # )
    # new_sub_competency.save()
    serilizer = SubCompetencyserializer(data=request.data)
    if serilizer.is_valid():
        serilizer.save()
    else:
        return Response({"status": "bad request"}, status=400)

    return Response({"status": "success"}, status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
def addCompitency(request):
    new_competency = Competency(
        name=request.data['name'],
    )
    new_competency.save()
    return Response({"status": "success"}, status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
def addCourseAssesment(request):
    serilizer = CourseAssesmentserializer(data=request.data)
    if serilizer.is_valid():
        serilizer.save()
    else:
        return Response({"status": "bad request"}, status=400)
    return Response({"status": "success"}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getCourseAssesment(request):
    assesment = CourseAssesment.objects.all()
    serilizer = CourseAssesmentserializer(assesment, many=True)
    return Response({"status": "success", "data": serilizer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getCourseAssesmentById(request, assesment_id):
    assesment = CourseAssesment.objects.get(id=assesment_id)
    serilizer = CourseAssesmentserializer(assesment)
    return Response({"status": "success", "data": serilizer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getCourseAssesmentByType(request, type):
    assesment = CourseAssesment.objects.filter(type=type)
    serilizer = CourseAssesmentserializer(assesment, many=True)
    return Response({"status": "success", "data": serilizer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getCompitency(request):
    competency = Competency.objects.all()
    serilizer = Competencyserializer(competency, many=True)
    return Response({"status": "success", "data": serilizer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getCompitencyById(request, comp_id):
    competency = Competency.objects.filter(id=comp_id)
    serilizer = Competencyserializer(competency, many=True)
    return Response({"status": "success", "data": serilizer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getSubCompitency(request):
    sub_competency = SubCompetency.objects.all()
    serilizer = SubCompetencyserializer(sub_competency, many=True)
    return Response({"status": "success", "data": serilizer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getSubCompitencyById(request, subcom_id):
    sub_competency = SubCompetency.objects.filter(id=subcom_id)
    serilizer = SubCompetencyserializer(sub_competency, many=True)
    return Response({"status": "success", "data": serilizer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getQuestionbyType(request, type):
    question = Question.objects.filter(type=type)
    serilizer = Questionserializer(question, many=True)
    return Response({"status": "success", "data": serilizer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getQuestion(request, type):
    question = Question.objects.all()
    serilizer = Questionserializer(question, many=True)
    return Response({"status": "success", "data": serilizer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getQuestionbyId(request, ques_id):
    question = Question.objects.filter(id=ques_id)
    serilizer = Questionserializer(question, many=True)
    return Response({"status": "success", "data": serilizer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getQuestionbySubCompetency(request, sub_competency):
    question = Question.objects.filter(sub_competency=sub_competency)
    serilizer = Questionserializer(question, many=True)
    return Response({"status": "success", "data": serilizer.data}, status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
def addCourseAssesmentLink(request):
    id = uuid.uuid4()
    print(str(id))
    if request.data['type'] == '360':
        new_assesment = {
            "name":request.data['name'],
            "type":request.data['type'],
            "course_assesment":request.data['course_assesment'],
            # "batch":request.data['batch'],
            "company":request.data['company'],
            "leader":request.data['leader'],
            "_id":str(id),
        }
    elif request.data['type'] == 'pre' or request.data['type'] == 'post':
        new_assesment = {
            "name":request.data['name'],
            "type":request.data['type'],
            "course_assesment":request.data['course_assesment'],
            "batch":request.data['batch'],
            "_id":str(id),
        }
    serilizer = AssesmentLinkserializer(data= new_assesment)
    if serilizer.is_valid():
        serilizer.save()
    else:
        print(serilizer.errors)
        return Response({"status": "bad request"}, status=400)
    return Response({"status": "success","data":serilizer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getCourseAssesmentLinkById(request, _id):
    assesment = Assesment.objects.filter(_id=_id)
    serilizer = AssesmentLinkserializer(assesment, many=True)
    return Response({"status": "success", "data": serilizer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getCourseAssesmentLinkByType(request, type):
    assesment = Assesment.objects.filter(type=type)
    serilizer = AssesmentLinkserializer(assesment, many=True)
    return Response({"status": "success", "data": serilizer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getCourseAssesmentLinkByLeader(request, leader_id):
    assesment = Assesment.objects.filter(id=leader_id)
    serilizer = AssesmentLinkserializer(assesment, many=True)
    return Response({"status": "success", "data": serilizer.data}, status=200)

@api_view(["POST"])
@permission_classes([AllowAny])
def addLeader(request):
    serializer = LeaderSerializer(data=request.data)
    email_message = render_to_string(
        "addcoachmail.html",
        {
            "coach_name": request.data["first_name"],
            "username": request.data["email"],
            "password": request.data["password"],
        },
    )
    if serializer.is_valid():
        newUser = User.objects.create_user(
            username=request.data["email"], email=request.data["email"], password=request.data["password"]
        )
        newUser.save()
        userToSave = User.objects.get(username=request.data["email"])
        newProfile = Profile(user=userToSave, type="leader",
                             email=request.data["email"])
        newProfile.save()
        serializer.save(user_id=newProfile.id)
        send_mail(
            # title:
            "You are added as a Leader on {title}".format(title="Meeraq"),
            # message:
            email_message,
            # from:0
            "info@meeraq.com",
            # to:
            [request.data["email"]],
            html_message=email_message,
        )
        for user in User.objects.all():
            token = Token.objects.get_or_create(user=user)
    else:
        print(serializer.errors)
        return Response(status="400")
    return Response({"status": 200, "payload": serializer.data, "token": str(token[0])})


@api_view(["GET"])
@permission_classes([AllowAny])
def getLeader(request, leader_id):
    leader = Leader.objects.filter(id=leader_id)
    serilizer = LeaderSerializer(leader, many=True)
    return Response({"status": "success", "data": serilizer.data}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getAllLeader(request):
    leader = Leader.objects.all()
    serilizer = LeaderSerializer(leader, many=True)
    return Response({"status": "success", "data": serilizer.data}, status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
def submmitedAssesment(request):
    for question in request.data['questions']:
        serilizer = SubmitedQuestionserializer(data=question)
        if serilizer.is_valid():
            serilizer.save()
        else:
            return Response({"status": "bad request"}, status=400)
    questions = SubmitedQuestion.objects.filter(gmail = request.data['assesment']['email'])
    
    ques_id = []
    for question in questions:
        ques_id.append(question.id)
    new_assesment = {
        "assesment" :  request.data['assesment']['assesment_name'],
        "question" : ques_id,
        "name" : request.data['assesment']['person_name'],
        "email" : request.data['assesment']['email'],
        "score" : request.data['assesment']['score']
    }
    sub_serilizer = SubmittedAssesmentserializer(data=new_assesment)
    if sub_serilizer.is_valid():
        sub_serilizer.save()
    else:
        return Response({"status": "bad request"}, status=400)
    return Response({"status": "success"}, status=200)




@api_view(["POST"])
@permission_classes([AllowAny])
def addPeopleByLeader(request):
    serilizer = AddpeopleByLeaderserializer(data = request.data)
    if serilizer.is_valid():
        serilizer.save()
    else:
        return Response({"status": "bad request"}, status=400)
    return Response({"status": "success"}, status=200)

from django.shortcuts import render

def view(request):
    lists = {
        "sc1":'hello',
        "sc2":5
    }

    # print(lists.keys())
    # content = "<div>"
    # for item in lists.keys():
    #     content = content + '<section>'
    #     content = content + "hello"
    #     content = content + '</section>'
    # content = content + '</div>'
    users = [{"compitency":'EI',"score":12},{"compitency":"ART","score":5}]    
    # print(content)
    my_context = {
        "my_list":lists,
        "len": users
    }

    # email_message = render_to_string(
    #     "submittedAssesment.html",
    #     my_context
    # )

    # send_mail(
    #         # title:
    #         "You are added as a Leader on {title}".format(title="Meeraq"),
    #         # message:
    #         email_message,
    #         # from:0
    #         "info@meeraq.com",
    #         # to:
    #         ['pankaj@meeraq.com'],
    #         html_message=email_message,
    #     )


    return render(request,"submittedAssesment.html",my_context)

