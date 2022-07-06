from django.urls import path
from . import views
urlpatterns = [
    path('', views.getCourses),
    path('addcourses/', views.addCourses),
    path('learners/', views.getLearners),
    path('addlearners/', views.addLearners),
]
