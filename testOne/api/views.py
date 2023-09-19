import uuid
import requests
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
from base.models import LeanerConfirmedSlots
from base.models import (
    Batch,
    Learner,
    EmailTemplate,
    SentEmail,
    UserToken,
    CalendarEvent,
)
from .serializers import (
    AdminReqSerializer,
    BatchSerializer,
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
    EmailTemplateSerializer,
    SentEmailSerializer,
    UserTokenSerializer,
    CalendarEventSerializer,
)
import requests
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.utils import timezone
from urllib.parse import urlencode
from django.core.exceptions import ObjectDoesNotExist
from testOne import settings
from django.utils.dateparse import parse_datetime
from django.utils.safestring import mark_safe
import json
import environ
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, ClockedSchedule

env = environ.Env()
environ.Env.read_env()


def convert_to_24hr_format(time_str):
    time_obj = datetime.strptime(time_str, "%I:%M %p")
    time_24hr = time_obj.strftime("%H:%M")
    return time_24hr


def refresh_microsoft_access_token(user_token):
    if not user_token:
        return None

    refresh_token = user_token.refresh_token
    access_token_expiry = user_token.access_token_expiry
    auth_code = user_token.authorization_code
    if not refresh_token:
        return None

    access_token_expiry = int(access_token_expiry)

    expiration_timestamp = user_token.updated_at + timezone.timedelta(
        seconds=access_token_expiry
    )

    if expiration_timestamp <= timezone.now():
        token_url = f"https://login.microsoftonline.com/{env('MICROSOFT_TENANT_ID')}/oauth2/v2.0/token"

        token_data = {
            "client_id": env("MICROSOFT_CLIENT_ID"),
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
            "client_secret": env("MICROSOFT_CLIENT_SECRET"),
        }

        response = requests.post(token_url, data=token_data)
        token_json = response.json()

        if "access_token" in token_json:
            user_token.access_token = token_json["access_token"]
            user_token.access_token_expiry = token_json.get("expires_in")
            user_token.updated_at = timezone.now()
            user_token.save()

            return user_token.access_token

    return user_token.access_token


def create_microsoft_calendar_event(
    access_token, event_details, attendee_email_name, event
):
    event_create_url = "https://graph.microsoft.com/v1.0/me/events"

    start_datetime = f"{event_details['startDate']}T{event_details['startTime']}"
    end_datetime = f"{event_details['startDate']}T{event_details['endTime']}"

    event_details_title = event_details["title"]

    event_payload = {
        "subject": event_details_title,
        "body": {"contentType": "HTML", "content": event_details["description"]},
        "start": {"dateTime": start_datetime, "timeZone": "UTC"},
        "end": {"dateTime": end_datetime, "timeZone": "UTC"},
        "attendees": [{"emailAddress": attendee_email_name, "type": "required"}],
    }

    user_token = UserToken.objects.get(access_token=access_token)
    new_access_token = refresh_microsoft_access_token(user_token)
    if not new_access_token:
        new_access_token = access_token

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.post(event_create_url, json=event_payload, headers=headers)

    if response.status_code == 201:
        microsoft_response_data = response.json()

        calendar_event = CalendarEvent(
            event_id=microsoft_response_data.get("id"),
            title=event_details_title,
            description=event_details.get("description"),
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            attendee=attendee_email_name.get("address"),
            creator=microsoft_response_data.get("organizer", {})
            .get("emailAddress", {})
            .get("address", ""),
            events=event,
            account_type="microsoft",
        )
        calendar_event.save()

        print("Event created successfully.")
        return True
    else:
        print(f"Event creation failed. Status code: {response.status_code}")
        print(response.text)
        return False


def delete_microsoft_calendar_event(access_token, event_id):
    try:
        event_delete_url = f"https://graph.microsoft.com/v1.0/me/events/{event_id}"

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.delete(event_delete_url, headers=headers)

        if response.status_code == 204:
            return {"message": "Event deleted successfully"}
        elif response.status_code == 404:
            return {"error": "Event not found"}
        else:
            return {
                "error": "Failed to delete event",
                "status_code": response.status_code,
            }

    except Exception as e:
        return {"error": "An error occurred", "details": str(e)}


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
            username=request.data["email"],
            email=request.data["email"],
            password=request.data["password"],
        )
        newUser.save()
        userToSave = User.objects.get(username=request.data["email"])
        newProfile = Profile(user=userToSave, type="coach", email=request.data["email"])
        newProfile.save()
        serializer.save(user_id=newProfile.id)
        send_mail(
            # title:
            "You are added as a Coach on {title}".format(title="Meeraq"),
            # message:
            email_message,
            # from:0
            settings.DEFAULT_FROM_EMAIL,
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
            if request.data["type"] == "coach":
                userProfile = Coach.objects.get(email=username)
                token = Token.objects.get_or_create(user=user)
                user_token = None
                try:
                    user_token = UserToken.objects.get(user_mail=username)
                    refresh_microsoft_access_token(user_token)

                except ObjectDoesNotExist:
                    print("Does not exist")
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
                    }
                )
            else:
                return Response({"reason": "No user found"}, status=404)
        elif user.profile.type == "admin":
            if request.data["type"] == "admin":
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
            username=request.data["email"],
            email=request.data["email"],
            password=request.data["password"],
        )
        newUser.save()
    else:
        return Response(status="403")
    user = User.objects.get(username=serializer.data["email"])
    userToSave = User.objects.get(username=serializer.data["email"])
    newProfile = Profile(user=userToSave, type="admin", email=serializer.data["email"])
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


# it take date str in "yyyy-mm-dd" format and returns in "dd-mm-yyyy"
def formatDate(date):
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%d-%m-%y")
    return formatted_date


@api_view(["POST"])
@permission_classes([AllowAny])
def makeSlotRequest(request):
    adminRequest = AdminRequest(
        name=request.data["request_name"], expire_date=request.data["expiry_date"]
    )
    adminRequest.save()
    formatted_date = formatDate(request.data["expiry_date"])
    for coach in request.data["coach_id"]:
        single_coach = Coach.objects.get(id=coach)
        email_message = render_to_string(
            "makerequest.html",
            {"expire_date": formatted_date, "coach_name": single_coach.first_name},
        )

        send_mail(
            # title:
            "Meeraq - Coaching Sessions Slot Requests",
            # message:
            email_message,
            # from:0
            settings.DEFAULT_FROM_EMAIL,
            # to:
            [single_coach.email],
            html_message=email_message,
        )
        adminRequest.assigned_coach.add(single_coach)
    for slot in request.data["slots"]:
        newSlot = SlotForCoach(
            start_time=slot["start_time"],
            end_time=slot["end_time"],
            date=slot["date"],
            request=adminRequest,
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
                expire_date=_request.expire_date
            ).first()
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
            if _request.isActive == True and (
                not checkIfCoachExistsInQuerySet(confirmedCoaches, coach_id)
            ):
                request_id_name[_request.id] = _request.name
                all_slots += SlotForCoach.objects.filter(request=_request)
        if type == "ACTIVE":
            if _request.isActive == True and checkIfCoachExistsInQuerySet(
                confirmedCoaches, coach_id
            ):
                request_id_name[_request.id] = _request.name
                all_slots += SlotForCoach.objects.filter(request=_request)
        if type == "PAST":
            if _request.isActive == False and checkIfCoachExistsInQuerySet(
                confirmedCoaches, coach_id
            ):
                request_id_name[_request.id] = _request.name
                all_slots += SlotForCoach.objects.filter(request=_request)
        if type == "MISSED":
            if _request.isActive == False and (
                not checkIfCoachExistsInQuerySet(confirmedCoaches, coach_id)
            ):
                request_id_name[_request.id] = _request.name
                all_slots += SlotForCoach.objects.filter(request=_request)

    serializers = SlotForCoachSerializer(all_slots, many=True)
    return Response(
        {"details": "success", "slots": serializers.data, "requests": request_id_name},
        status=200,
    )


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
            SESSION_START_TIME=datetime.fromtimestamp(start_timestamp).strftime(
                "%I:%M %p"
            ),
            SESSION_END_TIME=datetime.fromtimestamp(end_timestamp).strftime("%I:%M %p"),
            SESSION_DATE=datetime.fromtimestamp(int(start_timestamp)).strftime(
                "%d %B %Y"
            ),
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
        ConfirmedSlotsbyCoach.objects.filter(request_ID=request_id)
    )
    response = HttpResponse(dataset.xls, content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = 'attachment; filename="slots.xls"'
    return response


@api_view(["GET"])
@permission_classes([AllowAny])
def export_all(request):
    today = date.today()
    coach_slot_file = ConfirmedSlotResource()
    dataset = coach_slot_file.export(ConfirmedSlotsbyCoach.objects.all())
    response = HttpResponse(dataset.xls, content_type="application/vnd.ms-excel")
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
    print(str(request.data["start_time"]), type(str(request.data["start_time"])))
    newSlot = {
        "start_time": request.data["start_time"],
        "end_time": request.data["end_time"],
        "date": request.data["date"],
        "coach_id": slot.coach_id,
        "request_ID": int(slot.request_ID),
        "SESSION_START_TIME": datetime.fromtimestamp(start_timestamp).strftime(
            "%I:%M %p"
        ),
        "SESSION_END_TIME": datetime.fromtimestamp(end_timestamp).strftime("%I:%M %p"),
        "SESSION_DATE": datetime.fromtimestamp(start_timestamp).strftime("%d %B %Y"),
        "COACH_NAME": Coach.objects.get(id=slot.coach_id).first_name
        + " "
        + Coach.objects.get(id=slot.coach_id).middle_name
        + " "
        + Coach.objects.get(id=slot.coach_id).last_name,
        "DESCRIPTION": AdminRequest.objects.get(id=slot.request_ID).name,
        "CC": Coach.objects.get(id=slot.coach_id).email,
        "MEETING_LINK": Coach.objects.get(id=slot.coach_id).meet_link,
    }

    serializer = ConfirmedSlotsbyCoachSerializer(instance=slot, data=newSlot)
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
    return Response(
        {"status": "success, Data deleted", "data": serializer.data}, status=200
    )


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
        "batch": request.data["batch"],
    }
    serializer = EventSerializer(data=event_data)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)
        return Response(
            {"status": "400 Bad request", "reason": "Wrong data sent"}, status=400
        )
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
                return Response(
                    {"status": "error", "reason": "error in expire event"}, status=401
                )
    updated_events = Events.objects.filter(is_delete=False)
    serializer = EventSerializer(updated_events, many=True)
    return Response({"status": "success", "data": serializer.data}, status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
def editEvents(request, event_id):
    today = date.today()
    event = Events.objects.get(id=event_id)
    expire_check = event.is_expired
    if datetime.strptime(request.data["expire_date"], "%Y-%m-%d") > datetime.strptime(
        str(today), "%Y-%m-%d"
    ):
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
    }
    serializer = EventSerializer(instance=event, data=event_data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(
            {"status": "400 Bad request", "reason": "Wrong data sent"}, status=400
        )
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
        "is_expired": True,
    }
    serializer = EventSerializer(instance=event, data=new_event)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(
            {"status": "400 Bad request", "reason": "something went wrong"}, status=400
        )
    return Response({"status": "success, Data deleted"}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def getSlotsByEventID(request, event_id):
    event = Events.objects.get(_id=event_id)
    if event.is_delete == True:
        return Response(
            {"status": "404 not found", "reason": "data not found"}, status=404
        )
    else:
        all_slots = []
        for coach in event.coach.all():
            slots = ConfirmedSlotsbyCoach.objects.filter(coach_id=coach.id)
            for slot in slots:
                if slot.is_confirmed == False & slot.is_realeased == False:
                    all_slots.append(slot)
        serializer = ConfirmedSlotsbyCoachSerializer(all_slots, many=True)
        eventserializer = EventSerializer(event)
        return Response(
            {
                "status": "success",
                "slots": serializer.data,
                "event": eventserializer.data,
            },
            status=200,
        )


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
    learners = Learner.objects.filter(batch=event.batch, email=request.data["email"])
    if len(learners) == 0:
        return Response(
            {"status": "Error", "reason": "user may have entered different email"},
            status=405,
        )
    else:
        coach_slot = ConfirmedSlotsbyCoach.objects.get(id=slot_id)
        coach_slot_serializer = ConfirmedSlotsbyCoachSerializer(coach_slot)
        if coach_slot.is_confirmed == False:
            coach_data = Coach.objects.get(id=coach_slot.coach_id)
            booked_slot_coach = {**coach_slot_serializer.data, "is_confirmed": True}
            coach_serilizer = ConfirmedSlotsbyCoachSerializer(
                instance=coach_slot, data=booked_slot_coach
            )
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
            event_serializer = EventSerializer(instance=event, data=new_event_data)

            serializer = ConfirmedSlotsbyLearnerSerializer(data=Booked_slot)
            if serializer.is_valid():
                booked_slots = LeanerConfirmedSlots.objects.all()
                if request.data["warning"] == True:
                    if not bool(booked_slots):
                        serializer.save()
                    else:
                        for slot in booked_slots:
                            if (
                                slot.email.lower() == request.data["email"].lower()
                            ) and (event.id == slot.event.id):
                                return Response(
                                    {
                                        "status": "409 Bad request",
                                        "reason": "email already exist",
                                    },
                                    status=409,
                                )
                        if event_serializer.is_valid():
                            event_serializer.save()
                            serializer.save()
                        else:
                            return Response(
                                {
                                    "status": "400 bad request",
                                    "reason": "Failed to book the slot",
                                },
                                status=400,
                            )
            else:
                print(serializer.errors)
                return Response(
                    {"status": "400 Bad request", "reason": "wrong data sent"},
                    status=400,
                )

            if event_serializer.is_valid():
                event_serializer.save()
            else:
                print(event_serializer.errors)
            if coach_serilizer.is_valid():
                coach_serilizer.save()
            else:
                return Response(
                    {"status": "400 Bad request", "reason": "coach data is wrong"},
                    status=400,
                )

            start_time = datetime.fromtimestamp(
                (int(coach_slot.start_time) / 1000)
            )  # converting timestamp to date
            start = (
                (
                    start_time.replace(microsecond=0)
                    .astimezone(utc)
                    .replace(tzinfo=None)
                    .isoformat()
                    + "Z"
                )
                .replace(":", "")
                .replace("-", "")
            )
            end_time = datetime.fromtimestamp((int(coach_slot.end_time) / 1000))
            end = (
                (
                    end_time.replace(microsecond=0)
                    .astimezone(utc)
                    .replace(tzinfo=None)
                    .isoformat()
                    + "Z"
                )
                .replace(":", "")
                .replace("-", "")
            )

            date = datetime.fromtimestamp(
                (int(coach_slot.start_time) / 1000) + 19800
            ).strftime("%d %B %Y")

            start_time_for_mail = datetime.fromtimestamp(
                (int(coach_slot.start_time) / 1000) + 19800
            )

            email_message_learner = render_to_string(
                "addevent.html",
                {
                    "name": request.data["name"],
                    "time": start_time_for_mail.strftime("%I:%M %p"),
                    "duration": "30 Min",
                    "date": date,
                    "link": coach_data.meet_link,
                },
            )

            event_start_time = datetime.strptime(
                f"{start_time}", "%Y-%m-%d %H:%M:%S"
            ).strftime("%H:%M:%S")
            event_end_time = datetime.strptime(
                f"{end_time}", "%Y-%m-%d %H:%M:%S"
            ).strftime("%H:%M:%S")
            session_date = datetime.strptime(date, "%d %B %Y").strftime("%Y-%m-%d")

            try:
                coachee_user_token = UserToken.objects.get(
                    user_mail=request.data["email"]
                )
                event_detail = {
                    "title": f"Coaching Session",
                    "description": f"Session Link: {coach_data.meet_link}",
                    "startDate": session_date,
                    "startTime": event_start_time,
                    "endDate": session_date,
                    "endTime": event_end_time,
                }
                coachee_access_token = coachee_user_token.access_token

                coachee_access_token = refresh_microsoft_access_token(
                    coachee_user_token
                )

                create_microsoft_calendar_event(
                    coachee_access_token,
                    event_detail,
                    {
                        "address": coach_data.email,
                        "name": coach_data.first_name + " " + coach_data.last_name,
                    },
                    event,
                )

            except ObjectDoesNotExist:
                print("Coachee Does not exist")

            meet_link = coach_data.meet_link
            createIcs(start, end, meet_link)
            email = EmailMessage(
                "Meeraq | Coaching Session",
                email_message_learner,
                settings.DEFAULT_FROM_EMAIL,  # from email address
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

            coach_module_link = "https://coach.meeraq.com/"
            email_message_coach = render_to_string(
                "coachmail.html",
                {
                    "name": coach_data.first_name,
                    "time": start_time_for_mail.strftime("%I:%M %p"),
                    "duration": "30 Min",
                    "date": date,
                    "link": coach_module_link,
                    "participant_name": request.data["name"],
                },
            )

            createIcs(start, end, coach_module_link)

            try:
                coach_user_token = UserToken.objects.get(user_mail=coach_data.email)

                event_detail = {
                    "title": f"Coaching Session",
                    "description": f"Session Link: {coach_module_link}",
                    "startDate": session_date,
                    "startTime": event_start_time,
                    "endDate": session_date,
                    "endTime": event_end_time,
                }
                coach_access_token = coach_user_token.access_token

                coach_access_token = refresh_microsoft_access_token(coach_user_token)

                create_microsoft_calendar_event(
                    coach_access_token,
                    event_detail,
                    {
                        "address": request.data["email"],
                        "name": request.data["name"],
                    },
                    event,
                )

            except ObjectDoesNotExist:
                print("Coach Does not exist")

            email_for_coach = EmailMessage(
                "Meeraq | Coaching Session",
                email_message_coach,
                settings.DEFAULT_FROM_EMAIL,  # from email address
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
            return Response(
                {"status": "Error", "reason": "Slot is already Booked"}, status=408
            )


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
        "status": request.data["status"],
        "email": booked_slots.email,
        "phone_no": booked_slots.phone_no,
        "organisation": booked_slots.organisation,
        "event": booked_slots.event.id,
        "slot": booked_slots.slot.id,
    }
    serializer = ConfirmedSlotsbyLearnerSerializer(instance=booked_slots, data=newSlot)

    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data}, status=200)
    else:
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
        (int(booked_slots.slot.start_time) / 1000)
    )  # converting timestamp to date
    start = (
        (
            start_time.replace(microsecond=0)
            .astimezone(utc)
            .replace(tzinfo=None)
            .isoformat()
            + "Z"
        )
        .replace(":", "")
        .replace("-", "")
    )
    end_time = datetime.fromtimestamp((int(booked_slots.slot.end_time) / 1000))
    end = (
        (
            end_time.replace(microsecond=0)
            .astimezone(utc)
            .replace(tzinfo=None)
            .isoformat()
            + "Z"
        )
        .replace(":", "")
        .replace("-", "")
    )

    date = datetime.fromtimestamp(
        (int(booked_slots.slot.start_time) / 1000) + 19800
    ).strftime("%d %B %Y")
    start_time_for_mail = datetime.fromtimestamp(
        (int(booked_slots.slot.start_time) / 1000) + 19800
    )
    email_message_learner = render_to_string(
        "cancelEvent.html",
        {"time": start_time_for_mail, "date": date},
    )

    createCancledIcs(start, end)
    coach = Coach.objects.get(id=booked_slots.slot.coach_id)
    email = EmailMessage(
        "Meeraq | Canceled Coaching Session",
        email_message_learner,
        settings.DEFAULT_FROM_EMAIL,
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
    for learner in request.data["participent"]:
        is_exist = Learner.objects.filter(
            unique_check=learner["batch"] + "|" + learner["email"]
        )
        if len(is_exist) > 0:
            continue
        else:
            if "phone" in learner.keys():
                learner_data = Learner(
                    first_name=learner["first_name"],
                    last_name=learner["last_name"],
                    email=learner["email"],
                    batch=learner["batch"],
                    phone=learner["phone"],
                    unique_check=learner["batch"] + "|" + learner["email"],
                    course=learner["course"],
                )
            else:
                learner_data = Learner(
                    first_name=learner["first_name"],
                    last_name=learner["last_name"],
                    email=learner["email"],
                    batch=learner["batch"],
                    unique_check=learner["batch"] + "|" + learner["email"],
                    course=learner["course"],
                )
            learner_data.save()
            is_batch_exist = Batch.objects.filter(batch=learner["batch"])
            if not is_batch_exist:
                batches.add(learner["batch"])
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
    print("app access key", env("100MS_APP_ACCESS_KEY"))
    expires = 24 * 3600
    now = datetime.utcnow()
    exp = now + timedelta(seconds=expires)
    return jwt.encode(
        payload={
            "access_key": env("100MS_APP_ACCESS_KEY"),
            "type": "management",
            "version": 2,
            "jti": str(uuid.uuid4()),
            "iat": now,
            "exp": exp,
            "nbf": now,
        },
        key=env("100MS_APP_SECRET"),
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def getManagementToken(request):
    management_token = generateManagementToken()
    return Response(
        {"message": "Success", "management_token": management_token}, status=200
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def getCurrentBookedSlot(request):
    learner_email = request.data["learner_email"]
    meet_link = "https://coach.meeraq.com/join-session/" + request.data["room_id"]
    current_time = request.data["time"]
    today_date = datetime.date(datetime.today())
    try:
        coach = Coach.objects.get(meet_link=meet_link)
        try:
            booked_slot = LeanerConfirmedSlots.objects.get(
                slot__coach_id=coach.id, email=learner_email, slot__date=today_date
            )
            if (
                booked_slot
                and (current_time > (int(booked_slot.slot.start_time) - 300000))
                and (current_time < int(booked_slot.slot.end_time))
            ):
                booked_slot_serializer = ConfirmedLearnerSerializer(booked_slot)
                return Response(
                    {"message": "Success", "data": booked_slot_serializer.data},
                    status=200,
                )
            else:
                return Response({"No session found"}, status=401)
        except:
            return Response({"message": "No session found"}, status=401)
    except:
        return Response({"message": "Invalid Link"}, status=400)


@api_view(["GET"])
@permission_classes([AllowAny])
def exportLearnerConfirmedSlotsByEventId(request, event_id):
    confirmed_slot_file = LearnerConfirmedSlotsResource()
    dataset = confirmed_slot_file.export(
        LeanerConfirmedSlots.objects.filter(event=event_id)
    )
    response = HttpResponse(dataset.xls, content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = 'attachment; filename="confirmed slots.xls"'
    return response


@api_view(["GET"])
@permission_classes([AllowAny])
def getLearnersWithNoSessions(request, _id):
    try:
        event = Events.objects.get(_id=_id)
        batch = event.batch
        learners = Learner.objects.filter(batch=batch)

        learners_with_no_sessions = []

        for learner in learners:
            sessions = LeanerConfirmedSlots.objects.filter(
                email=learner.email, event=event
            )

            if len(sessions) == 0:
                learners_with_no_sessions.append(learner.email)

        return Response(
            {
                "learners_with_no_sessions": learners_with_no_sessions,
                "total_learners": len(learners_with_no_sessions),
                "details": "success",
            },
            status=200,
        )

    except Events.DoesNotExist:
        return Response({"error": "Event not found"}, status=404)


@api_view(["POST"])
@permission_classes([AllowAny])
def sendEmailsToLearners(request):
    data = request.data
    recipient_emails = data.get("recipient_emails", [])
    if not recipient_emails:
        return Response({"error": "Recipient emails not provided"}, status=400)
    try:
        event = Events.objects.get(_id=data.get("event_id", ""))
    except Exception as e:
        return Response({"message": "Failed to send link to learners."}, status=400)
    scheduled_for = data.get("scheduled_for", datetime.now())
    clocked = ClockedSchedule.objects.create(
        clocked_time=scheduled_for
    )  # time is utc one here
    recipient_emails_json = json.dumps(recipient_emails)
    print("recipient_emails_json", recipient_emails_json, type(recipient_emails_json))
    periodic_task = PeriodicTask.objects.create(
        name=uuid.uuid1(),
        task="base.tasks.send_event_link_to_learners",
        args=[event.id],
        clocked=clocked,
        one_off=True,
    )
    event.sent_to_participants.append({"date": int(datetime.now().timestamp() * 1000)})
    event.save()
    return Response(
        {
            "sent_emails": recipient_emails,
            "total_sent": len(recipient_emails),
            "details": "success",
        },
        status=200,
    )


# @api_view(["POST"])
# @permission_classes([AllowAny])
# def send_mails(request):
#     emails = request.data.get('emails',[])
#     subject = request.data.get('subject')
#     print(emails, "emailsssssssss")
#     print(subject, "subjectttttt")
#     # email_content = request.data['email_content']
#     temp1=request.data.get('htmlContent','')
#     if len(emails) > 0:
#         for email in emails:
#             email_message_learner = render_to_string(
#                 "default.html",
#                 {
#                     'email_content': mark_safe(temp1),
#                     'email_title': "hello"
#                     'subject': (subject)
#                 },
#             )
#             email = EmailMessage(
#                 "Meeraq",
#                 email_message_learner,
#                 settings.DEFAULT_FROM_EMAIL,  # from email address
#                 [email],  # to email address
#                 # [coach_data.email],  # bcc email address
#                 # headers={"Cc": ["info@meeraq.com"]}  # setting cc email address
#             )
#             email.content_subtype = "html"
#             email.send()
#             print('hello')
#             # send mail
#         return Response({"message":"success"},status=200)
#     return Response({'error': "No email found."},status=400)


@api_view(["POST"])
@permission_classes([AllowAny])
def send_test_mails(request):
    emails = request.data.get("emails", [])
    subject = request.data.get("subject")
    # email_content = request.data.get('email_content', '')  # Assuming you're sending email content too
    temp1 = request.data.get("htmlContent", "")

    print(emails, "emails")

    # if not subject:
    #     return Response({'error': "Subject is required."}, status=400)

    if len(emails) > 0:
        for email in emails:
            email_message_learner = render_to_string(
                "default.html",
                {
                    "email_content": mark_safe(temp1),
                    "email_title": "hello",
                    "subject": subject,
                },
            )
            email = EmailMessage(
                subject,
                email_message_learner,
                settings.DEFAULT_FROM_EMAIL,  # from email address
                [email],  # to email address
            )
            email.content_subtype = "html"
            email.send()
            print("Email sent to:", email)

        return Response({"message": "Emails sent successfully"}, status=200)
    else:
        return Response({"error": "No email addresses found."}, status=400)


@api_view(["POST"])
@permission_classes([AllowAny])
def send_mails(request):
    subject = request.data.get("subject")
    scheduled_for = request.data.get("scheduledFor", "")
    recipients_data = request.data.get("recipients_data", [])
    try:
        template = EmailTemplate.objects.get(id=request.data.get("template_id", ""))
        if len(recipients_data) > 0:
            sent_email_instance = SentEmail(
                recipients=recipients_data,
                subject=subject,
                template=template,
                status="pending",
                scheduled_for=scheduled_for,
            )
            sent_email_instance.save()
            clocked = ClockedSchedule.objects.create(
                clocked_time=scheduled_for
            )  # time is utc one here
            periodic_task = PeriodicTask.objects.create(
                name=uuid.uuid1(),
                task="base.tasks.send_email_to_recipients",
                args=[sent_email_instance.id],
                clocked=clocked,
                one_off=True,
            )
            sent_email_instance.periodic_task = periodic_task
            sent_email_instance.save()
            return Response({"message": "Emails sent successfully"}, status=200)
        else:
            return Response({"error": "No email addresses found."}, status=400)
    except EmailTemplate.DoesNotExist:
        return Response({"error": "Failed to schedule emails"}, status=400)


@api_view(["POST"])
@permission_classes([AllowAny])
def addEmailTemplate(request):
    if request.method == "POST":
        title = request.data.get("title", None)
        template_data = request.data.get("templatedata", None)
        print(title, "Title")
        print(template_data, "request.data")

        if template_data is not None:
            try:
                email_template = EmailTemplate.objects.create(
                    title=title, template_data=template_data
                )
                # email_template = EmailTemplate.objects.create(title=title, template_data=template_data)
                # (template_data=template_data,template_title)
                print(email_template, "email template")
                return Response(
                    {"success": True, "message": "Template saved successfully."}
                )
            except Exception as e:
                return Response(
                    {"success": False, "message": "Failed to save template."}
                )

    return Response({"success": False, "message": "Invalid request."})


@api_view(["PUT"])
@permission_classes([AllowAny])
def editEmailTemplate(request, template_id):
    try:
        email_template = EmailTemplate.objects.get(pk=template_id)
    except EmailTemplate.DoesNotExist:
        return Response(
            {"success": False, "message": "Template not found."}, status=404
        )

    if request.method == "PUT":
        title = request.data.get("title", None)
        template_data = request.data.get("templatedata", None)
        print(template_data, "request.data")

        if template_data is not None:
            try:
                email_template.title = title
                email_template.template_data = template_data
                email_template.save()
                return Response(
                    {"success": True, "message": "Template updated successfully."}
                )
            except Exception as e:
                return Response(
                    {"success": False, "message": "Failed to update template."}
                )

    return Response({"success": False, "message": "Invalid request."})


@api_view(["GET"])
@permission_classes([AllowAny])
def getSavedTemplates(request):
    emailTemplate = EmailTemplate.objects.all()
    serilizer = EmailTemplateSerializer(emailTemplate, many=True)
    return Response({"status": "success", "data": serilizer.data}, status=200)


@api_view(["DELETE"])
@permission_classes([AllowAny])
def deleteEmailTemplate(request, template_id):
    try:
        delete_template = EmailTemplate.objects.get(pk=template_id)
        delete_template.delete()
        return Response({"success": True, "message": "Template deleted successfully."})
    except EmailTemplate.DoesNotExist:
        return Response(
            {"success": False, "message": "Template not found."}, status=404
        )
    except Exception as e:
        return Response({"success": False, "message": "Failed to delete template."})


@api_view(["GET"])
@permission_classes([AllowAny])
def get_mail_data(request):
    sent_emails = SentEmail.objects.all()
    print(sent_emails)
    serializer = SentEmailSerializer(sent_emails, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([AllowAny])
def cancel_scheduled_mail(request, sent_mail_id):
    try:
        sent_email = SentEmail.objects.get(id=sent_mail_id)
    except SentEmail.DoesNotExist:
        return Response({"error": "Scheduled email not found."}, status=404)

    if sent_email.status == "cancelled":
        return Response({"error": "Email is already cancelled."}, status=400)
    if sent_email.status == "completed":
        return Response({"error": "Email is already sent."}, status=400)

    sent_email.status = "cancelled"
    sent_email.save()

    return Response({"message": "Email has been successfully cancelled."})


@api_view(["GET"])
@permission_classes([AllowAny])
def pending_scheduled_mails_exists(request, email_template_id):
    sent_emails = SentEmail.objects.filter(
        template__id=email_template_id, status="pending"
    )
    return Response({"exists": sent_emails.count() > 0}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def microsoft_auth(request, user_mail_address):
    oauth2_endpoint = f"https://login.microsoftonline.com/{env('MICROSOFT_TENANT_ID')}/oauth2/v2.0/authorize"

    auth_params = {
        "client_id": env("MICROSOFT_CLIENT_ID"),
        "response_type": "code",
        "redirect_uri": env("MICROSOFT_REDIRECT_URI"),
        "response_mode": "query",
        "scope": "openid offline_access User.Read Calendars.ReadWrite profile email",
        "state": "shashankmeeraq",
        "login_hint": user_mail_address,
    }

    auth_url = f"{oauth2_endpoint}?{urlencode(auth_params)}"

    return HttpResponseRedirect(auth_url)


@api_view(["POST", "GET"])
@permission_classes([AllowAny])
def microsoft_callback(request):
    try:
        authorization_code = request.GET.get("code")

        token_url = f"https://login.microsoftonline.com/common/oauth2/v2.0/token"
        token_data = {
            "client_id": env("MICROSOFT_CLIENT_ID"),
            "scope": "User.Read",
            "code": authorization_code,
            "redirect_uri": env("MICROSOFT_REDIRECT_URI"),
            "grant_type": "authorization_code",
            "client_secret": env("MICROSOFT_CLIENT_SECRET"),
        }

        response = requests.post(token_url, data=token_data)

        token_json = response.json()

        if "access_token" in token_json and "refresh_token" in token_json:
            access_token = token_json["access_token"]
            refresh_token = token_json["refresh_token"]
            expires_in = token_json["expires_in"]
            auth_code = authorization_code
            user_email_url = "https://graph.microsoft.com/v1.0/me"
            headers = {"Authorization": f"Bearer {access_token}"}

            user_email_response = requests.get(user_email_url, headers=headers)

            if user_email_response.status_code == 200:
                user_info_data = user_email_response.json()
                user_email = user_info_data.get("mail", "")

                user_token, created = UserToken.objects.get_or_create(
                    user_mail=user_email
                )
                user_token.access_token = access_token
                user_token.refresh_token = refresh_token
                user_token.access_token_expiry = expires_in
                user_token.authorization_code = auth_code
                user_token.account_type = "microsoft"
                user_token.save()

            coach_exists = Coach.objects.filter(email=user_email)
            if coach_exists:
                return HttpResponseRedirect(env("coach_url"))
            return HttpResponseRedirect(env("learner_url"))

        else:
            error_json = response.json()
            return JsonResponse(error_json, status=response.status_code)

    except Exception as e:
        # Handle exceptions here, you can log the exception for debugging
        print(f"An exception occurred: {str(e)}")
        # You might want to return an error response or redirect to an error page.
        return JsonResponse({"error": "An error occurred"}, status=500)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_courses(request):
    api_key = env("THINKIFIC_API_KEY")
    subdomain = env("THINKIFIC_SUBDOMAIN")

    api_url = "https://api.thinkific.com/api/public/v1/courses?page=1&limit=200"
    headers = {
        "X-Auth-API-Key": api_key,
        "X-Auth-Subdomain": subdomain,
        "Content-Type": "application/json",
    }
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return Response(data)
        else:
            return Response(
                {"error": "Failed to fetch data from Thinkific"},
                status=response.status_code,
            )
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=500)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_enrollments(request, course_id):
    api_key = "4048d97cded22462166590c24cccd1ab"
    subdomain = "meeraq-s-site-18a1"

    api_url = f"https://api.thinkific.com/api/public/v1/enrollments/?query[course_id]={course_id}"
    headers = {
        "X-Auth-API-Key": api_key,
        "X-Auth-Subdomain": subdomain,
        "Content-Type": "application/json",
    }
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return Response(data)
        else:
            return Response(
                {"error": "Failed to fetch data from Thinkific"},
                status=response.status_code,
            )
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=500)
