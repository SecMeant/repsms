from django.conf.urls import url
from django.contrib import admin
from .views import main ,renderclass
urlpatterns = [
    url(r'^$', main),
    url(r'^(?P<classPro>(\w)+)$', renderclass),
]
