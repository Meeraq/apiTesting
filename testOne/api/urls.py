from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.getcoach, name="get_course"),
    path("coaches/", views.getcoach, name="get_coaches"),
    path("add-coaches/", views.addcoach, name="add_coaches"),
    path("update-coach/<str:_id>/", views.updateCoach, name="update_coach"),
    path("login/", views.login_user),
    path("register/", views.registerUser),
    path("make-request/", views.makeSlotRequest),
    path("get-requested-slots/<str:coach_id>/<str:type>/", views.getSlotofRequest),
    path(
        "confirm-available-slots-by-coach/<str:coach_id>/<str:request_id>/",
        views.confirmAvailableSlotsByCoach,
    ),
    path("export-confirmed-slot-data/<str:request_id>/", views.export),
    path("export-all-confirmed-slot-data/", views.export_all),
    path(
        "get-confirmed-slots-by-coach/<str:coach_id>/", views.getConfirmedSlotsbyCoach
    ),
    path(
        "get-confirmed-slots-by-request/<str:req_id>/",
        views.getConfirmedSlotsbyRequestID,
    ),
    path("edit-confirmed-slots/<str:slot_id>/", views.updateConfirmedSlots),
    path(
        "delete-confirmed-slots-by-coach/<str:coach_id>/<str:slot_id>/",
        views.deleteConfirmedSlotsbyCoach,
    ),
    path("get-admin-request/", views.getAdminRequestData, name="get_admin_request"),
    path("update-meetlink-by-coach/<str:_id>/", views.updateMeetLinkByCoach),
    path("delete-request/<str:req_id>/", views.deleteRequest),
    # path('file-import/', ExportImportExcel.as_view()),
    path(
        "password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    path("add-event/", views.addEvent),
    path("events/", views.getEvents),
    path("edit-event/<str:event_id>/", views.editEvents),
    path("delete-event/<str:event_id>/", views.deleteEvents),
    path("get-slots-by-event-id/<str:event_id>/", views.getSlotsByEventID),
    path("confirm-slot-by-learner/<str:slot_id>/", views.confirmSlotsByLearner),
    path("get-booked-slots-by-learner/", views.getConfirmSlotsByLearner),
    path(
        "get-booked-slots-of-learner-event-id/<str:event_id>/",
        views.getConfirmSlotsByLearnerByEventId,
    ),
    path(
        "delete-booked-slots-of-learner/<str:slot_id>/", views.deleteConfirmSlotsAdmin
    ),
    path(
        "booked-slot-by-coach/<str:coach_id>/", views.getLearnerConfirmedSlotsByCoachId
    ),
    path(
        "update-session-status/<str:slot_id>/", views.editConfirmSlotsByLearnerBySlotId
    ),
    path("learner-upload/", views.learnerDataUpload),
    path("get-batches/", views.getBatches),
    path("get-learner-by-batch/<str:batch_id>/", views.getLearnerBatchwise),
    path("management-token/", views.getManagementToken),
    path("current-booked-slot/", views.getCurrentBookedSlot),
    path(
        "export-confirmed-slot/<str:event_id>",
        views.exportLearnerConfirmedSlotsByEventId,
    ),
    path("send_mails/", views.send_mails),
    path("send_test_mails/", views.send_test_mails),
    path("save_template/", views.addEmailTemplate),
    path("saved_emailsTemplates/", views.getSavedTemplates),
    path("edit_email_template/<int:template_id>/", views.editEmailTemplate),
    path("delete_email_template/<int:template_id>/", views.deleteEmailTemplate),
    path("emails-data/", views.get_mail_data),
    path("cancel-schedule-email/<int:sent_mail_id>/", views.cancel_scheduled_mail),
    path(
        "pending-scheduled-mails/<int:email_template_id>/",
        views.pending_scheduled_mails_exists,
    ),
    path("get-learners-with-no-sessions/<str:_id>/", views.getLearnersWithNoSessions),
    path("send-emails-to-learners/", views.sendEmailsToLearners),
    path("microsoft/oauth/<str:user_mail_address>/", views.microsoft_auth),
    path("microsoft-auth-callback/", views.microsoft_callback),
    path("get_courses_from_thinkific/", views.get_courses),
    path(
        "get_participants_by_course/<int:course_id>/",
        views.get_enrollments,
        name="get_enrollments",
    ),
    path("upcoming-sessions/", views.get_upcoming_sessions),
    path(
        "confirmed-slots-of-coach/",
        views.get_all_confirmed_slots,
        name="all-confirmed-slots",
    ),
]
