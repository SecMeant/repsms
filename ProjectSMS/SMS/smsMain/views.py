from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import addProfile, addStudent
import os
import sqlite3
from .csvfuncs import searchcsv, importcsv

# Create your views here.
@login_required
@transaction.atomic
def smsApp(request):
	
	if request.user.is_authenticated:
		current_user = request.user

		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		dbname = current_user.username
		dbname += ".sqlite3"
		conn = sqlite3.connect(os.path.join(BASE_DIR, current_user.username + '.sqlite3'))
		formAddProfile = addProfile
		formAddStudent = addStudent

		if request.method == 'POST':
			if "addStudent" in request.POST:
				formAddStudent = addStudent(request.POST)
				if formAddStudent.is_valid():
					imieUcznia = formAddStudent.cleaned_data['imie']
					nazwiskoUcznia = formAddStudent.cleaned_data['nazwisko']
					peselUcznia = formAddStudent.cleaned_data['pesel']
					c = conn.cursor()
					c.execute("CREATE TABLE IF NOT EXISTS uczniowie(imie text, nazwisko text, pesel text)")
					c.execute("INSERT INTO uczniowie VALUES(?,?,?)",(imieUcznia,nazwiskoUcznia,peselUcznia))
					conn.commit()
					conn.close()
					context={
						"current_user" : current_user,
						"formAddProfile":formAddProfile,
						"formAddStudent":formAddStudent,
					}
					return render (request, "SMS.html", context)

			elif "studentFile" in request.POST:

				#Tablica szukanych kolumn w pliku csv

				wantedtable = [
					"Imię", #1
					"Nazwisko",#2
					"Kod pocztowy",#3
					"Miejscowość",#4
					"Ulica",#5
					"Nr budynku",#6
					"Nr mieszkania",#7
					"angielski",#8
					"niemiecki",#9
					]

				answer = [None] * len(wantedtable)
				c = conn.cursor()

				file = request.FILES['studentFile']
				line = file.readline().decode('utf-8')
				fline = line.split(";")

				i=0
				for word in wantedtable:
					answer[i] = searchcsv(word,request.FILES['studentFile'])
					i+=1

				importcsv(wantedtable,answer,request.FILES['studentFile'],c)


				context={
						"current_user" : current_user,
						"formAddProfile":formAddProfile,
						"formAddStudent":formAddStudent,
					}

				return render (request, "SMS.html", context)

			elif "addProfile" in request.POST:
				formAddProfile = addProfile(request.POST)
				if formAddProfile.is_valid():
					fullname = formAddProfile.cleaned_data['newProfileFullName']
					shortname = formAddProfile.cleaned_data['newProfileShortName']
					c = conn.cursor()
					c.execute("CREATE TABLE IF NOT EXISTS profile(fullname text, shortname text)")
					c.execute("SELECT * FROM profile")
					same = False
					for row in c.fetchall():
						if (row[0] == fullname or row[1] == shortname):
							same = True
							break
					if(same == False):
						c.execute("INSERT INTO profile VALUES(?,?)",(fullname,shortname))
					conn.commit()
					conn.close()
					context={
						"current_user" : current_user,
						"formAddProfile":formAddProfile,
						"formAddStudent":formAddStudent,
						"same":same
					}
					return render (request, "SMS.html", context)
		context={
			"current_user" : current_user,
			"formAddProfile":formAddProfile,
			"formAddStudent":formAddStudent,
		}
		return render (request, "SMS.html", context)