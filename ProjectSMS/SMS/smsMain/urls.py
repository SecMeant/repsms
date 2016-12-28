from django.conf.urls import url
from django.contrib import admin
from .views import smsApp , showAllStudents , showAllStudentsWithClass , showAllStudentsWithNoClass
urlpatterns = [
    url(r'^$', smsApp),
    url(r'^wszyscyuczniowie', showAllStudents),
    url(r'^uczniowieprzydzieleni', showAllStudentsWithClass),
    url(r'^uczniowienieprzydzieleni', showAllStudentsWithNoClass),
]
