from django.urls import path
from .views import ApplicationUploadView, ApplicationReadView, AnswerUpdateDeleteView, AnswerSubmitView

urlpatterns = [
    path("", ApplicationReadView, name="application_read_default"),
    path("<int:application_id>", ApplicationReadView, name="application_read"),
    path("upload", ApplicationUploadView, name="application_upload"),
    path("practice", AnswerUpdateDeleteView, name="practice"),
    path("submit", AnswerSubmitView, name="submit"),
]