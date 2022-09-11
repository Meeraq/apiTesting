from django.conf.urls import url
from django.urls import path

from task.views import generate

urlpatterns = [
    url('generate/', generate, name='generate')
]