from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path('', views.getCourses,name='get_course'),
    path('add-courses/', views.addCourses,name='add_course'),
    path('update-courses/<str:_id>/', views.updateCourses,name='update_course'),
    path('learners/', views.getLearners,name='get_learner'),
    path('add-learner/', views.addLearners,name='add_learner'),
    path('update-learner/<str:_id>/', views.updateLearners,name='update_learner'), 
    path('batchs/', views.addBatches),
    path('add-batchs/', views.getBatches),
    path('update-batch/<str:_id>/', views.updateBatches,name='update_batch'),
    path('coaches/', views.getcoach),
    path('add-coaches/', views.addcoach),
    path('update-coach/<str:_id>/', views.updateCoach,name='update_coach'),
    path('faculty/', views.getfaculty),
    path('add-faculty/', views.addfaculty),
    path('update-faculty/<str:_id>/', views.updateFaculty,name='update_faculty'),
    path('avilable-slot/', views.getslot),
    path('add-slots/', views.addslot),
    path('add-time-day-slot/', views.addDayTimeslot),
    path('time-day-slot/', views.getDayTimeslot),
    path('update-time-day-slot/<str:_id>/', views.updateDayTimeslot,name='update_time_day_slot'),
    path('delete-time-day-slot/<str:_id>/', views.deleteDayTimeslot),
    path('file-import/', ExportImportExcel.as_view()),
]
