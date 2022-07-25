from django.urls import path
from . import views
urlpatterns = [
    path('', views.getCourses),
    path('addcourses/', views.addCourses),
    path('learners/', views.getLearners),
    path('addlearners/', views.addLearners),
    path('addBatchs/', views.addBatches),
    path('coaches/', views.getcoach),
    path('addcoaches/', views.addcoach),
    path('faculty/', views.getfaculty),
    path('addfaculty/', views.addfaculty),
    path('avilableslot/', views.getslot),
    path('addslots/', views.addslot),
]
