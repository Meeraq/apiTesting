from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.getCourses, name='get_course'),
    path('add-courses/', views.addCourses, name='add_course'),
    path('update-courses/<str:_id>/', views.updateCourses, name='update_course'),
    path('course-category/', views.getCourseCategory),
    path('learners/', views.getLearners, name='get_learner'),
    path('add-learner/', views.addLearners, name='add_learner'),
    path('update-learner/<str:_id>/', views.updateLearners, name='update_learner'),
    path('batchs/', views.getBatches, name='get_batch'),
    path('add-batchs/', views.addBatches, name='add_batch'),
    path('update-batch/<str:_id>/', views.updateBatches, name='update_batch'),
    path('coaches/', views.getcoach, name='get_coaches'),
    path('add-coaches/', views.addcoach, name='add_coaches'),
    path('update-coach/<str:_id>/', views.updateCoach, name='update_coach'),
    path('faculty/', views.getfaculty, name="get_faculty"),
    path('add-faculty/', views.addfaculty, name="add_faculty"),
    path('update-faculty/<str:_id>/', views.updateFaculty, name='update_faculty'),
    path('avilable-slot/', views.getslot),
    path('add-slots/', views.addslot),
    path('add-time-day-slot/', views.addDayTimeslot),
    path('confirm-day-time-slot/', views.confirmDayTimeSlot),
    path('time-day-slot/', views.getDayTimeslot),
    path('update-time-day-slot/<str:_id>/',
         views.updateDayTimeslot, name='update_time_day_slot'),
    path('delete-time-day-slot/<str:_id>/', views.deleteDayTimeslot),
    path('learner-time-day-slot/', views.learnergetDayTimeslot),
    path('delete-learner-time-day-slot/<str:_id>/',
         views.LearnerdeleteDayTimeslot),
    path('update-learner-time-day-slot/<str:_id>/',
         views.updateLearnerDayTimeslot, name='update_learner_time_day_slot'),
    path('add-learner-time-day-slot/', views.addLearnerDayTimeslot),
    path('session/', views.getSessions),
    path('add-session/', views.addSession),
    path('login/', views.login_user),
    path('register/', views.registerUser),
    path('add-user-type/', views.addProfileType),
    path('user-type/', views.getProfile),

    path('get-available-learner-slots', views.getAvailableSlots),
    path('pick-learner-slot', views.pickLearnerSlot),
    path('get-learner-slot/', views.getLearnerSlot),

    path('time-table', views.getCoachCoacheeSessions),

    # sesame link
    path("login-learner/", views.loginLearner, name="email_login"),
    path("trial/", views.trialLogin, name="trial"),
    path('make-request/', views.makeSlotRequest),
    path('get-requested-slots/<str:coach_id>/<str:type>/', views.getSlotofRequest),
    path('confirm-available-slots-by-coach/<str:coach_id>/<str:request_id>/',
         views.confirmAvailableSlotsByCoach),
    path('export-confirmed-slot-data/<str:request_id>/', views.export),
    path('export-all-confirmed-slot-data/', views.export_all),
    path('get-confirmed-slots-by-coach/<str:coach_id>/',
         views.getConfirmedSlotsbyCoach),
    path('get-confirmed-slots-by-request/<str:req_id>/',
         views.getConfirmedSlotsbyRequestID),
    path('edit-confirmed-slots/<str:slot_id>/', views.updateConfirmedSlots),
    path('delete-confirmed-slots-by-coach/<str:coach_id>/<str:slot_id>/',
         views.deleteConfirmedSlotsbyCoach),
    path('get-admin-request/', views.getAdminRequestData),
    # path('file-import/', ExportImportExcel.as_view()),



    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

]
