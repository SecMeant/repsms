from django.conf.urls import url
from django.contrib import admin
from .views import index,confirm

urlpatterns = [
    url(r'^$', index),
    url(r'^confirm/$', confirm),
]
