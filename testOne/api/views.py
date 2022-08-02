from rest_framework.response import Response
# import pandas as pd
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from base.models import Courses,Learners,Batch,Coach,Faculty,Slot,DayTimeSlot,LearnerdayTimeSlot,Sessions,customUser
# from base.models import ExcelFileUpload
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .serializers import CourseSerializer,LearnerSerializer,BatchSerializer,CoachSerializer,FacultySerializer,SlotSerializer,SlotTimeDaySerializer,LearnerSlotTimeDaySerializer,SessionSerializer,UserSerializer





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


@api_view(['POST'])

def updateCourses(request,_id):
    course = Courses.objects.get(id=_id)
    serializer = CourseSerializer(instance=course,data=request.data)
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



@api_view(['POST'])

def updateLearners(request,_id):
    learner = Learners.objects.get(id=_id)
    serializer = LearnerSerializer(instance=learner,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

#batch api

@api_view(['GET'])

def getBatches(request):
    batches = Batch.objects.all()
    serializer = BatchSerializer(batches,many=True)
    return Response(serializer.data)

@api_view(['POST'])

def addBatches(request):
    serializer = BatchSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])

def updateBatches(request,_id):
    batch = Batch.objects.get(id=_id)
    serializer = BatchSerializer(instance=batch,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


#coach api

@api_view(['GET'])

def getcoach(request):
    coaches = Coach.objects.all()
    serializer = CoachSerializer(coaches,many=True)
    return Response(serializer.data)


# class RegisterUser(APIView):
#     def post(self,request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         else:
#             print(serializer.errors)
#             return Response(status='403')
#         user = User.objects.get(username = serializer.data['username'])
#         token , _ = Token.objects.get_or_create(user=user)
#         print(customUser.objects.all())
#         return Response({'status': 200,'payload':serializer.data,'token':str(token)})

@api_view(['POST'])

def addcoach(request):
    serializer = CoachSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        newUser = User(username=serializer.data['name'],password = 'Nish@@nt111')
        newUser.save()
    else:
        print(serializer.errors)
        return Response(status='403')
    for user in User.objects.all():
        token = Token.objects.get_or_create(user=user)
    return Response({'status': 200,'payload':serializer.data,'token':str(token)})


@api_view(['POST'])

def updateCoach(request,_id):
    coach = Coach.objects.get(id=_id)
    serializer = CoachSerializer(instance=coach,data=request.data)
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

def updateFaculty(request,_id):
    faculty = Faculty.objects.get(id=_id)
    serializer = FacultySerializer(instance=faculty,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

#slot api

@api_view(['GET'])

def getslot(request):
    slots = Slot.objects.all()
    serializer = SlotSerializer(slots,many=True)
    return Response(serializer.data)


@api_view(['POST'])

def addslot(request):
    serializer = SlotSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])

def getDayTimeslot(request):
    slots = DayTimeSlot.objects.all()
    serializer = SlotTimeDaySerializer(slots,many=True)
    return Response(serializer.data)


@api_view(['POST'])

def addDayTimeslot(request):
    for day in request.data:
            newdayTimeSlot =  DayTimeSlot(coach=day['coach'],dayofmock = day['dayofmock'],start_time_id = day['start_time_id'], end_time_id = day['end_time_id'])
            newdayTimeSlot.save()

    slots = DayTimeSlot.objects.all()
    serializer = SlotTimeDaySerializer(slots,many=True)
    return Response({'status':200,'data':serializer.data})

@api_view(['POST'])

def updateDayTimeslot(request,_id):
    slot = DayTimeSlot.objects.get(id=_id)
    serializer = SlotTimeDaySerializer(instance=slot,data=request.data)
    if serializer.is_valid():
        serializer.save()

    slots = DayTimeSlot.objects.all()
    serializer = SlotTimeDaySerializer(slots,many=True)
    return Response({'status': 200,'data':serializer.data})


@api_view(['DELETE'])

def deleteDayTimeslot(request,_id):
    slot = DayTimeSlot.objects.get(id=_id)
    slot.delete()

    slots = DayTimeSlot.objects.all()
    serializer = SlotTimeDaySerializer(slots,many=True)
    return Response({'status': 200,'data':serializer.data})

#learner slot book


@api_view(['GET'])

def learnergetDayTimeslot(request):
    slots = LearnerdayTimeSlot.objects.all()
    serializer = LearnerSlotTimeDaySerializer(slots,many=True)
    return Response(serializer.data)


@api_view(['POST'])

def addLearnerDayTimeslot(request):
    for day in request.data:
            newdayTimeSlot =  LearnerdayTimeSlot(learner=day['learner'],start_time_id = day['start_time_id'], end_time_id = day['end_time_id'])
            newdayTimeSlot.save()
    slots = LearnerdayTimeSlot.objects.all()
    serializer = LearnerSlotTimeDaySerializer(slots,many=True)
    return Response({'status':200,'data':serializer.data})

@api_view(['POST'])

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

def getSessions(request):
    session = Sessions.objects.all()
    serializer = SessionSerializer(session,many=True)
    return Response(serializer.data)


@api_view(['POST'])

def addSession(request):
    serializer = SessionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(status='500')
    return Response(serializer.data)











# class ExportImportExcel(APIView):
#     def post(self,request):
#         exceled_upload_obj = ExcelFileUpload.objects.create(excel_file_upload=request.FILES['files'])
#         df = pd.read_csv(f"{settings.BASE_DIR}/{exceled_upload_obj.excel_file_upload}")
#         print(df.values.tolist())
#         return Response({'status': 200})