from django.conf.urls import url
from django.contrib import admin
from .views import smsApp , showAllStudents , showAllStudentsWithClass , showAllStudentsWithNoClass, showSpecificClass , manageStudents, deleteStudentsFromClass, editStudent, deleteWholeClass

urlpatterns = [
	url(r'^$', smsApp),
	url(r'^wszyscyuczniowie$', showAllStudents),
	url(r'^uczniowieprzydzieleni$', showAllStudentsWithClass),
	url(r'^uczniowienieprzydzieleni$', showAllStudentsWithNoClass),
	url(r'^zarzadzanieuczniami$', manageStudents),
	url(r'^edytujucznia/(?P<id>\d+)$', editStudent),
	url(r'^usunucznia/(?P<id>\d+)$', deleteStudentsFromClass),
	url(r'^delklasa/(?P<klasa>\w{0,50}$)', deleteWholeClass),
	url(r'^klasa/(?P<klasa>\w{0,50}$)', showSpecificClass),
]
