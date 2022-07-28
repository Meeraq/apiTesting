from rest_framework.response import Response
# import pandas as pd
from django.conf import settings
# from rest_framework.views import APIView
from rest_framework.decorators import api_view
from base.models import Courses,Learners,Batch,Coach,Faculty,slot,dayTimeSlot
# from base.models import ExcelFileUpload
from .serializers import CourseSerializer,LearnerSerializer,BatchSerializer,CoachSerializer,FacultySerializer,SlotSerializer,SlotTimeDaySerializer
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
    serializer = LearnerSerializer(batches,many=True)
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


@api_view(['POST'])

def addcoach(request):
    serializer = CoachSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

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
    slots = slot.objects.all()
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
    slots = dayTimeSlot.objects.all()
    serializer = SlotTimeDaySerializer(slots,many=True)
    return Response(serializer.data)


@api_view(['POST'])

def addDayTimeslot(request):
    for day in request.data:
            newdayTimeSlot =  dayTimeSlot(coach=day['coach'],dayofmock = day['day'],start_time_id = day['startID'], end_time_id = day['endID'])
            newdayTimeSlot.save()
    return Response({'status':200})

@api_view(['POST'])

def updateDayTimeslot(request,_id):
    slot = dayTimeSlot.objects.get(id=_id)
    serializer = SlotTimeDaySerializer(instance=slot,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response({'status': 200})


@api_view(['DELETE'])

def deleteDayTimeslot(request,_id):
    slot = dayTimeSlot.objects.get(id=_id)
    slot.delete()
    return Response({'status': 200})


# class ExportImportExcel(APIView):
#     def post(self,request):
#         exceled_upload_obj = ExcelFileUpload.objects.create(excel_file_upload=request.FILES['files'])
#         df = pd.read_csv(f"{settings.BASE_DIR}/{exceled_upload_obj.excel_file_upload}")
#         print(df.values.tolist())
#         return Response({'status': 200})