from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import addProfile, addStudent, addClass, addAlgorithm, removeClass, removeProfile, removeAlgorithm, fillClass
from .funkcjeopty import dejnumer, optymalizuj, rest
from .fillfuncs import fillclasses 
import os
import sqlite3
import math
from .csvfuncs import searchcsv, importcsv
from django.contrib.auth import logout
from operator import itemgetter

@login_required
@transaction.atomic
def smsApp(request):
	
	if request.user.is_authenticated:

		if  request.user.is_expired():
			print(request.user.is_active)
			logout(request)
			HttpResponseRedirect('/')


		current_user = request.user

		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		dbname = current_user.username
		dbname += ".sqlite3"
		conn = sqlite3.connect(BASE_DIR + '\\userData\\' + current_user.username + '.sqlite3')
		

		c = conn.cursor()

		# Preparing data to send it to forms
		# Algorithms choicefield
		# Need to do this that way because of the manner of django functions.
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
		# I want to leave a nice comment to line under for loop, becouse its a true beauty !
		# im iterating data in loop as usual, appending a ClassId just after casting to string from integer
		# than adding a '-' and concatenating name of the class to display it in a list, 
		# the class id is the value passed to remove method later
		# Im adding '-' because the name of class can contain spaces and im calling split() fucntion to
		# make this work like this [(a),(b)] - like multidimensinal array, because the choiceField function requires that
		# so by adding a dash im making sure that the split will happen just between right data.
		# After all im not sure of im doing this concatenate the right way, but im just a python begginer so..
		c.execute("SELECT * FROM klasy")
		klasy = c.fetchall()
		klasypass = []
		for cols in klasy:
			klasypass.append((str(cols[5])+"-"+cols[0]).split("-"))

		c.execute("SELECT * FROM uczniowie")
		uczniowie = c.fetchall()
		klasyPostfix = []
		for uczen in uczniowie:
			if( not( vectorContains(klasyPostfix,uczen[len(uczen)-1]) ) ):
				klasyPostfix.append(uczen[len(uczen)-1])

		formAddProfile = addProfile
		formAddStudent = addStudent
		formAddAlgorithm = addAlgorithm
		formRemoveProfile = removeProfile(profile=(profiles))
		formAddClass = addClass(profile=(profiles),algorytm=(algorithmspass))
		formRemoveClass = removeClass(klasy=(klasypass))
		formRemoveAlgorithm = removeAlgorithm(algorytm=(algorithmspass))
		formFillClass = fillClass(klasy=(klasypass))

		context={
			"current_user":current_user,
			"formAddProfile":formAddProfile,
			"formAddStudent":formAddStudent,
			"formAddClass":formAddClass,
			"formAddAlgorithm":formAddAlgorithm,
			"formRemoveClass":formRemoveClass,
			"formRemoveProfile":formRemoveProfile,
			"formRemoveAlgorithm":formRemoveAlgorithm,
			"formFillClass":formFillClass,
			"klasyPostfix":klasyPostfix,
		}

		if request.method == 'POST':
			# Dodawanie ucznia, pojedyncze
			if "addStudent" in request.POST:
				formAddStudent = addStudent(request.POST)
				if formAddStudent.is_valid():


					#There was one csv that instead of blank fields had actual 'null' string in it
					#It causes some problems in fill / opt functions
					for key,value in formAddStudent.cleaned_data.items():
						if(value == 'null'):
							formAddStudent.cleaned_data[key] = 0

					imieUcznia = formAddStudent.cleaned_data['imie']
					nazwiskoUcznia = formAddStudent.cleaned_data['nazwisko']
					kod1Ucznia = formAddStudent.cleaned_data['kod1']
					kod2Ucznia = formAddStudent.cleaned_data['kod2']
					kodUcznia1 = kod1Ucznia +'-'+ kod2Ucznia
					miejscowoscUcznia = formAddStudent.cleaned_data['miejscowosc']
					ulicaUcznia = formAddStudent.cleaned_data['ulica']
					nrbudynkuUcznia = formAddStudent.cleaned_data['nrbudynku']
					nrmieszkaniaUcznia = formAddStudent.cleaned_data['nrmieszkania']
					kod12Ucznia = formAddStudent.cleaned_data['kod12']
					kod22Ucznia = formAddStudent.cleaned_data['kod22']
					kodUcznia2 = kod12Ucznia +'-'+ kod22Ucznia
					miejscowosc2Ucznia = formAddStudent.cleaned_data['miejscowosc2']
					ulica2Ucznia = formAddStudent.cleaned_data['ulica2']
					nrbudynku2Ucznia = formAddStudent.cleaned_data['nrbudynku2']
					nrmieszkania2Ucznia = formAddStudent.cleaned_data['nrmieszkania2']
					ocenaPolskiUcznia = formAddStudent.cleaned_data['ocenPol']
					ocenaMatematykaUcznia = formAddStudent.cleaned_data['ocenMat']
					ocenaAngielskiUcznia = formAddStudent.cleaned_data['ocenAng']
					ocenaNiemieckiUcznia = formAddStudent.cleaned_data['ocenNiem']

					c = conn.cursor()
					c.execute("INSERT INTO uczniowie (Imię,Nazwisko,Kod_pocztowy,Miejscowość,Ulica,Nr_budynku,Nr_mieszkania,Kod_pocztowy2,Miejscowość2,Ulica2,Nr_budynku2,Nr_mieszkania2,polski,matematyka,angielski,niemiecki) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(imieUcznia,nazwiskoUcznia,kodUcznia1,miejscowoscUcznia,ulicaUcznia,nrbudynkuUcznia,nrmieszkaniaUcznia,kodUcznia2,miejscowosc2Ucznia,ulica2Ucznia,nrbudynku2Ucznia,nrmieszkania2Ucznia,ocenaMatematykaUcznia,ocenaPolskiUcznia,ocenaAngielskiUcznia,ocenaNiemieckiUcznia))
					conn.commit()
					conn.close()
					
					context.update({"formAddStudent":formAddStudent})
					return HttpResponseRedirect("/sms/extended")

					# Dodawanie klasy

			elif "addClass" in request.POST:
				formAddClass =  addClass(request.POST,profile=(profiles),algorytm=(algorithmspass))
				if formAddClass.is_valid():
					nazwaKlasy = formAddClass.cleaned_data['nazwaKlasy']
					profil = formAddClass.cleaned_data['profil']
					liczebnosc = formAddClass.cleaned_data['liczebnosc']
					algorytm = formAddClass.cleaned_data['algorytm']	
					c = conn.cursor()
					c.execute("INSERT INTO klasy VALUES(?,?,?,?,?,?)",(nazwaKlasy,profil,liczebnosc,algorytm,'A',None))
					conn.commit()
					conn.close()

					context.update({"formAddClass":formAddClass})
					return HttpResponseRedirect("/sms/extended")

					# Wypelnianie klasy

			elif "fillClass" in request.POST:
				formFillClass = fillClass(request.POST,klasy=(klasypass))
				if formFillClass.is_valid():
					c = conn.cursor()
					sposob = formFillClass.cleaned_data['sposob']
					c.execute("SELECT * FROM klasy WHERE id=" + formFillClass.cleaned_data['klasy'])
					klasa = c.fetchall()

					c.execute("SELECT * FROM uczniowie WHERE klasa IS NULL")

					uczniowie = c.fetchall()
					uczniowie = list(map(list,uczniowie))

					# start of implementation of opti functions from php
					ile = len(uczniowie)
					if(ile>=1 and sposob==True):
						odp = []
						odpowiedzi = [] # I have no idea why i chose similar names. Have no time to figure it out right now
						sizeofclass = int(klasa[0][2])
						odpowiedzi.append(dejnumer(ile,sizeofclass)) # First argument is size of all students to sort out, secound is size of class
						odp.append(optymalizuj(odpowiedzi[0],sizeofclass)) # Same arguments as above here
						print("DEBUG INFORMATION:")
						print("odp1:")
						print(odp)
						odp[0] = rest(odp[0]) # Here as argument I need returned value from optymalizuj function
						print("odpowiedzi:")
						print(odpowiedzi)
						print("odp:")
						print(odp)
						print("END OF DEBUG")
						fillclasses(c,conn,klasa,uczniowie,current_user,odp)

					else:
						fillclasses(c,conn,klasa,uczniowie,current_user,0)
					# end of implementation

					context.update({"formFillClass":formFillClass})
					return HttpResponseRedirect("/sms/extended")

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

					context.update({"formRemoveClass":formRemoveClass})
					return HttpResponseRedirect("/sms/extended")

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

					context.update({"formRemoveProfile":formRemoveProfile})
					return HttpResponseRedirect("/sms/extended")
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
					"polski",#8
					"angielski",#9
					"niemiecki",#10
					"francuski",#11
					"wloski",#12
					"hiszpanski",#13
					"rosyjski",#14
					"matematyka",#15
					"fizyka",#16
					"informatyka",#17
					"historia",#18
					"biologia",#19
					"chemia",#20
					"geografia",#21
					"wos",#22
					"zajęcia techniczne",#23
					"zajęcia artstyczne",#24
					"edukacja dla bezpieczeństwa",#25
					"plastyka",#26
					"muzyka",#27
					"wf",#28
					"zachowanie",#29
					]

				answer = []
				c = conn.cursor()

				for word in wantedtable:
					temp = searchcsv(word,request.FILES['studentFile'])
					if(temp != None):
						answer.append(searchcsv(word,request.FILES['studentFile']))
					else:
						answer.append('')

				print(answer)
				importcsv(wantedtable,answer,request.FILES['studentFile'],c)

				conn.commit()
				conn.close()

				return HttpResponseRedirect("/sms/extended")
				# Dodawanie profilu

			elif "addProfile" in request.POST:
				formAddProfile = addProfile(request.POST)
				if formAddProfile.is_valid():
					fullname = formAddProfile.cleaned_data['newProfileFullName']
					shortname = formAddProfile.cleaned_data['newProfileShortName']
					c = conn.cursor()
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

					context.update({"formAddProfile":formAddProfile,"same":same})
					return HttpResponseRedirect("/sms/extended")

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
					c.execute("CREATE TABLE IF NOT EXISTS algorytmy(id integer NOT NULL PRIMARY KEY AUTOINCREMENT, nazwa text, jpolski integer, matematyka integer, jangielski integer, jniemiecki integer)")
					c.execute("SELECT * FROM algorytmy")
					same = False
					for row in c.fetchall():
						if (row[1] == nazwaAlgo):
							same = True
							break
					if(same == False):
						c.execute("INSERT INTO algorytmy VALUES(?,?,?,?,?,?)",(None,nazwaAlgo,matematyka,jpolski,jangielski,jniemiecki))
					conn.commit()
					conn.close()

					context.update({"formAddAlgorithm":formAddAlgorithm})
					return HttpResponseRedirect("/sms/extended")

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

					context.update({"formRemoveAlgorithm":formRemoveAlgorithm})
					return HttpResponseRedirect("/sms/extended")

		return render (request, "SMS.html", context)

def showAllStudents(request):
	if request.user.is_authenticated:
		if  request.user.is_expired():
			print(request.user.is_active)
			logout(request)
			HttpResponseRedirect('/')

		current_user = request.user

		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		dbname = current_user.username
		dbname += ".sqlite3"
		conn = sqlite3.connect(BASE_DIR + '\\userData\\' + current_user.username + '.sqlite3')
		c = conn.cursor()

		c.execute("SELECT * FROM uczniowie")
		allStudents = c.fetchall()
		headerTable = [description[0] for description in c.description]

		context={
			"allStudents":allStudents,
			"headerTable":headerTable,
		}

		return render (request, "allStudents.html",context)
def collectclasses(c,current_user):
	c.execute("SELECT * FROM klasy")
	classes = c.fetchall()
	className = []
	for everyclass in classes:
		letter = 'A'
		while(everyclass[4] >= letter):
			className.append(str(current_user) + str(everyclass[0]) + letter)
			letter = ord(letter)
			letter += 1
			letter = chr(letter)
	return className

def showAllStudentsWithClass(request):
	if request.user.is_authenticated:
		if  request.user.is_expired():
			print(request.user.is_active)
			logout(request)
			HttpResponseRedirect('/')

		current_user = request.user

		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		dbname = current_user.username
		dbname += ".sqlite3"
		conn = sqlite3.connect(BASE_DIR + '\\userData\\' + current_user.username + '.sqlite3')
		c = conn.cursor()

		c.execute("SELECT * FROM uczniowie")
		allStudents = c.fetchall()
		headerTable = [description[0] for description in c.description]

		classList = collectclasses(c,current_user)
		
		# THIS QUERY IS TEMPORARY !!! THIS CAN PROVIDE CRASHES IN THE FUTUTRE
		# Im getting all the fields with NULL
		# but this value for no class might change in the future
		# so im just targeting it worth looking sometime when crash occurs.,
		classes = []
		for each in classList:
			query = "SELECT * FROM uczniowie WHERE klasa='"+each+"'"
			c.execute(query) 
			classes.append(c.fetchall())

		context={
			"classes":classes,
			"headerTable":headerTable,
		}

		return render (request, "studentsWithClass.html",context)

def showAllStudentsWithNoClass(request):
	if request.user.is_authenticated:
		if  request.user.is_expired():
			print(request.user.is_active)
			logout(request)
			HttpResponseRedirect('/')

		current_user = request.user

		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		dbname = current_user.username
		dbname += ".sqlite3"
		conn = sqlite3.connect(BASE_DIR + '\\userData\\' + current_user.username + '.sqlite3')
		c = conn.cursor()

		c.execute("SELECT * FROM uczniowie WHERE klasa IS NULL")
		allStudents = c.fetchall()

		headerTable = [description[0] for description in c.description]
		
		context={
			"allStudents":allStudents,
			"headerTable":headerTable,
		}

		return render (request, "studentsWithNoClass.html", context)

def vectorContains(tab,phrase):
	for each in tab:
		if(each == phrase):
			return 1
	return 0