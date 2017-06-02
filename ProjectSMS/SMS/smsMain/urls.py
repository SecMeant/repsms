from django.conf.urls import url
from django.contrib import admin
from .views import smsApp , showAllStudents , showAllStudentsWithClass , showAllStudentsWithNoClass, test , manageStudents, deleteStudentsFromClass
urlpatterns = [
	url(r'^$', smsApp),
	url(r'^wszyscyuczniowie$', showAllStudents),
	url(r'^uczniowieprzydzieleni$', showAllStudentsWithClass),
	url(r'^uczniowienieprzydzieleni$', showAllStudentsWithNoClass),
	url(r'^zarzadzanieuczniami$', manageStudents),
	url(r'^usunucznia/(?P<id>\d+)$', deleteStudentsFromClass),
	url(r'^test/(?P<klasa>\w{0,50}$)', test),
]
