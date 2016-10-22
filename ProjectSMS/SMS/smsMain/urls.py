from django.conf.urls import url
from django.contrib import admin
from .views import smsApp
urlpatterns = [
    url(r'^$', smsApp),
]
