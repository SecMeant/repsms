from django.conf.urls import url
from django.contrib import admin
from .views import index,confirm,remember,OWnLogout

urlpatterns = [
    url(r'^$', index),
    url(r'^confirm/$', confirm),
    url(r'^remind/$', remember),
    url(r'^logout/$', OWnLogout),
]
