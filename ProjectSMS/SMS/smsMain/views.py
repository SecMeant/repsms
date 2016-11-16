from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import addProfile, addStudent, addClass, addAlgorithm, removeClass, removeProfile, removeAlgorithm
import os
import sqlite3
from .csvfuncs import searchcsv, importcsv

@login_required
@transaction.atomic
def smsApp(request):
	
	if request.user.is_authenticated and request.user.is_expired():
		current_user = request.user

		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		dbname = current_user.username
		dbname += ".sqlite3"
		conn = sqlite3.connect(os.path.join(BASE_DIR, current_user.username + '.sqlite3'))
		c = conn.cursor()

		# Preparing data to send it to forms
		# Algorithms choicefield
		# Need to do this that way becouse of the manner of django functions.
		# forms.choicefield gets an array that contains only 2 indexes
		# first one contains name and the secound value of the select tag that is rendered by mentioned function
		c.execute("SELECT * FROM algorytmy")
		algorithms = c.fetchall()	
		algorithmspass = []
		for cols in algorithms:
			algorithmspass.append(cols[0:2]) 
		# Profiles choicefield
		c.execute("SELECT * FROM profile")
		profiles = c.fetchall()
		# Classes choicefield (removal)
		# I want to leave a nice comment to line under for loop, becouse its true beauty !
		# im iterating data in loop as usual, appending a ClassId just after casting to string from integer
		# than adding a '-' and concatenating name of the class to display it in a list, 
		# the class id is the value passed to remove method later
		# Im adding '-' becouse the name of class can contains spaces and im calling split() fucntion to
		# make this work like this [(a),(b)] like multidimensinal array, becouse the choiceField function requires that
		# so by adding a dash im making sure that the split will happen just between right data.
		# After all im not sure of im doing this concatenate the right way, but im just a python begginer so..
		c.execute("SELECT * FROM klasy")
		klasy = c.fetchall()
		klasypass = []
		for cols in klasy:
			klasypass.append((str(cols[4])+"-"+cols[0]).split("-"))

		formAddProfile = addProfile
		formAddStudent = addStudent
		formAddAlgorithm = addAlgorithm
		formRemoveProfile = removeProfile(profile=(profiles))
		formAddClass = addClass(profile=(profiles),algorytm=(algorithmspass))
		formRemoveClass = removeClass(klasy=(klasypass))
		formRemoveAlgorithm = removeAlgorithm(algorytm=(algorithmspass))

		if request.method == 'POST':
			# Dodawanie ucznia, pojedyncze
			if "addStudent" in request.POST:
				formAddStudent = addStudent(request.POST)
				if formAddStudent.is_valid():
					imieUcznia = formAddStudent.cleaned_data['imie']
					nazwiskoUcznia = formAddStudent.cleaned_data['nazwisko']
					c = conn.cursor()
					c.execute("CREATE TABLE IF NOT EXISTS uczniowie(imie text, nazwisko text , pesel integer, id integer NOT NULL PRIMARY KEY AUTOINCREMENT )")
					c.execute("INSERT INTO uczniowie ('Imię','Nazwisko') VALUES(?,?)",(imieUcznia,nazwiskoUcznia))
					conn.commit()
					conn.close()
					context={
						"current_user" : current_user,
						"formAddProfile":formAddProfile,
						"formAddStudent":formAddStudent,
						"formAddClass":formAddClass,
						"formAddAlgorithm":formAddAlgorithm,
						"formRemoveClass":formRemoveClass,
						"formRemoveProfile":formRemoveProfile,
						"formRemoveAlgorithm":formRemoveAlgorithm,
					}
					return render (request, "SMS.html", context)

					# Dodawanie klasy

			elif "addClass" in request.POST:
				formAddClass =  addClass(request.POST,profile=(profiles),algorytm=(algorithmspass))
				if formAddClass.is_valid():
					nazwaKlasy = formAddClass.cleaned_data['nazwaKlasy']
					profil = formAddClass.cleaned_data['profil']
					liczebnosc = formAddClass.cleaned_data['liczebnosc']
					algorytm = formAddClass.cleaned_data['algorytm']	
					c = conn.cursor()
					c.execute("CREATE TABLE IF NOT EXISTS klasy(nazwaKlasy text NOT NULL, profil text NOT NULL, liczebnosc integer NOT NULL, algorytm integer NOT NULL, id integer NOT NULL PRIMARY KEY AUTOINCREMENT )")
					c.execute("INSERT INTO klasy VALUES(?,?,?,?,?)",(nazwaKlasy,profil,liczebnosc,algorytm,None))
					conn.commit()
					conn.close()

					context={
						"current_user" : current_user,
						"formAddProfile":formAddProfile,
						"formAddStudent":formAddStudent,
						"formAddClass":formAddClass,
						"formAddAlgorithm":formAddAlgorithm,
						"formRemoveClass":formRemoveClass,
						"formRemoveProfile":formRemoveProfile,
						"formRemoveAlgorithm":formRemoveAlgorithm,
					}

					return render (request, "SMS.html", context)

					# Usuwanie klasy

			elif "removeClass" in request.POST:
				formRemoveClass =  removeClass(request.POST,klasy=(klasypass))
				if formRemoveClass.is_valid():
					idKlasy = formRemoveClass.cleaned_data['klasy']	
					c = conn.cursor()
					query = ""
					query = "DELETE FROM klasy WHERE id =" + idKlasy
					c.execute(query)
					conn.commit()
					conn.close()

					context={
						"current_user" : current_user,
						"formAddProfile":formAddProfile,
						"formAddStudent":formAddStudent,
						"formAddClass":formAddClass,
						"formAddAlgorithm":formAddAlgorithm,
						"formRemoveClass":formRemoveClass,
						"formRemoveProfile":formRemoveProfile,
						"formRemoveAlgorithm":formRemoveAlgorithm,
					}

					return render (request, "SMS.html", context)

				# Usuwanie profilu
					
			elif "removeProfile" in request.POST:
				formRemoveProfile =  removeProfile(request.POST,profile=(profiles))
				if formRemoveProfile.is_valid():
					profil = formRemoveProfile.cleaned_data['profile']	
					c = conn.cursor()
					query = ""
					query = "DELETE FROM profile WHERE shortname ='" + profil +"'"
					c.execute(query)
					conn.commit()
					conn.close()

					context={
						"current_user" : current_user,
						"formAddProfile":formAddProfile,
						"formAddStudent":formAddStudent,
						"formAddClass":formAddClass,
						"formAddAlgorithm":formAddAlgorithm,
						"formRemoveClass":formRemoveClass,
						"formRemoveProfile":formRemoveProfile,
						"formRemoveAlgorithm":formRemoveAlgorithm,
					}

					return render (request, "SMS.html", context)



					# Dodawanie ucznia / uczniow poprzez plik

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

				

				i=0
				for word in wantedtable:
					answer[i] = searchcsv(word,request.FILES['studentFile'])
					i+=1

				importcsv(wantedtable,answer,request.FILES['studentFile'],c)

				conn.commit()
				conn.close()
				context={
						"current_user" : current_user,
						"formAddProfile":formAddProfile,
						"formAddStudent":formAddStudent,
						"formAddClass":formAddClass,
						"formAddAlgorithm":formAddAlgorithm,
						"formRemoveClass":formRemoveClass,
						"formRemoveProfile":formRemoveProfile,
						"formRemoveAlgorithm":formRemoveAlgorithm,
					}

				return render (request, "SMS.html", context)

				# Dodawanie profilu

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
						c.execute("INSERT INTO profile VALUES(?,?)",(shortname,fullname))
					conn.commit()
					conn.close()
					context={
						"current_user" : current_user,
						"formAddProfile":formAddProfile,
						"formAddStudent":formAddStudent,
						"formAddClass":formAddClass,
						"formAddAlgorithm":formAddAlgorithm,
						"formRemoveClass":formRemoveClass,
						"same":same,
						"formRemoveProfile":formRemoveProfile,
						"formRemoveAlgorithm":formRemoveAlgorithm,
					}
					return render (request, "SMS.html", context)

					# Dodawanie algorytmu

			elif "addAlgorithm" in request.POST:
				formAddAlgorithm = addAlgorithm(request.POST)
				if formAddAlgorithm.is_valid():
					nazwaAlgo = formAddAlgorithm.cleaned_data['nazwa']
					matematyka = formAddAlgorithm.cleaned_data['matematyka']
					jpolski = formAddAlgorithm.cleaned_data['jpolski']
					jangielski = formAddAlgorithm.cleaned_data['jangielski']
					jniemiecki = formAddAlgorithm.cleaned_data['jniemiecki']
					c = conn.cursor()
					c.execute("CREATE TABLE IF NOT EXISTS algorytmy(id integer NOT NULL PRIMARY KEY AUTOINCREMENT, nazwa text, matematyka integer, jpolski integer, jangielski integer, jniemiecki integer)")
					c.execute("INSERT INTO algorytmy VALUES(?,?,?,?,?,?)",(None,nazwaAlgo,matematyka,jpolski,jangielski,jniemiecki))
					conn.commit()
					conn.close()
					context={
						"current_user" : current_user,
						"formAddProfile":formAddProfile,
						"formAddStudent":formAddStudent,
						"formAddClass":formAddClass,
						"formAddAlgorithm":formAddAlgorithm,
						"formRemoveClass":formRemoveClass,
						"formRemoveProfile":formRemoveProfile,
						"formRemoveAlgorithm":formRemoveAlgorithm,
					}
					return render (request, "SMS.html", context)

					# Usuwanie profilu
					
			elif "removeAlgorithm" in request.POST:
				formRemoveAlgorithm =  removeAlgorithm(request.POST,algorytm=(algorithmspass))
				if formRemoveAlgorithm.is_valid():
					algoName = formRemoveAlgorithm.cleaned_data['algorithm']	
					c = conn.cursor()
					query = ""
					query = "DELETE FROM algorytmy WHERE id =" + algoName
					print(query)
					c.execute(query)
					conn.commit()
					conn.close()

					context={
						"current_user" : current_user,
						"formAddProfile":formAddProfile,
						"formAddStudent":formAddStudent,
						"formAddClass":formAddClass,
						"formAddAlgorithm":formAddAlgorithm,
						"formRemoveClass":formRemoveClass,
						"formRemoveProfile":formRemoveProfile,
						"formRemoveAlgorithm":formRemoveAlgorithm,
					}

					return render (request, "SMS.html", context)



		context={
			"current_user" : current_user,
			"formAddProfile":formAddProfile,
			"formAddStudent":formAddStudent,
			"formAddClass":formAddClass,
			"formAddAlgorithm":formAddAlgorithm,
			"formRemoveClass":formRemoveClass,
			"formRemoveProfile":formRemoveProfile,
			"formRemoveAlgorithm":formRemoveAlgorithm,
		}
		return render (request, "SMS.html", context)