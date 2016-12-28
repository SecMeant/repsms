from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import addProfile, addStudent, addClass, addAlgorithm, removeClass, removeProfile, removeAlgorithm, fillClass
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

		formAddProfile = addProfile
		formAddStudent = addStudent
		formAddAlgorithm = addAlgorithm
		formRemoveProfile = removeProfile(profile=(profiles))
		formAddClass = addClass(profile=(profiles),algorytm=(algorithmspass))
		formRemoveClass = removeClass(klasy=(klasypass))
		formRemoveAlgorithm = removeAlgorithm(algorytm=(algorithmspass))
		formFillClass = fillClass(klasy=(klasypass))

		if request.method == 'POST':
			# Dodawanie ucznia, pojedyncze
			if "addStudent" in request.POST:
				formAddStudent = addStudent(request.POST)
				if formAddStudent.is_valid():
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

					context={
						"current_user" : current_user,
						"formAddProfile":formAddProfile,
						"formAddStudent":formAddStudent,
						"formAddClass":formAddClass,
						"formAddAlgorithm":formAddAlgorithm,
						"formRemoveClass":formRemoveClass,
						"formRemoveProfile":formRemoveProfile,
						"formRemoveAlgorithm":formRemoveAlgorithm,
						"formFillClass":formFillClass,
					}
					return HttpResponseRedirect("/sms")

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
					context={
						"current_user" : current_user,
						"formAddProfile":formAddProfile,
						"formAddStudent":formAddStudent,
						"formAddClass":formAddClass,
						"formAddAlgorithm":formAddAlgorithm,
						"formRemoveClass":formRemoveClass,
						"formRemoveProfile":formRemoveProfile,
						"formRemoveAlgorithm":formRemoveAlgorithm,
						"formFillClass":formFillClass,
					}

					return HttpResponseRedirect("/sms")

					# Wypelnianie klasy

			elif "fillClass" in request.POST:
				formFillClass = fillClass(request.POST,klasy=(klasypass))
				if formFillClass.is_valid():
					c = conn.cursor()
					print(formFillClass.cleaned_data['klasy'])
					c.execute("SELECT * FROM klasy WHERE id=" + formFillClass.cleaned_data['klasy'])
					klasa = c.fetchall()

					c.execute("SELECT * FROM uczniowie WHERE klasa IS NULL")

					uczniowie = c.fetchall()
					uczniowie = list(map(list,uczniowie))

					c.execute("SELECT * FROM algorytmy WHERE id="+str(klasa[0][3]))
					algo = c.fetchall()

					points = 0
					buff = 0
					print(len(uczniowie[0]))
					while(buff < len(uczniowie)):
						if(uczniowie[buff][13]):
							points = int(uczniowie[buff][13]) * algo[0][2]
						if(uczniowie[buff][14]):
							points += int(uczniowie[buff][14]) * algo[0][3]
						if(uczniowie[buff][15]):
							points += int(uczniowie[buff][15]) * algo[0][4]
						if(uczniowie[buff][16]):
							points += int(uczniowie[buff][16]) * algo[0][5]

						uczniowie[buff].append(points)
						buff += 1

					uczniowie = sorted(uczniowie,key=itemgetter(18),reverse=True)

					letter = klasa[0][4]

					inc = 0
					inc2 = 0
					j = 0
					while(inc < math.ceil(len(uczniowie)/klasa[0][2])):
						if(ord(letter)>90):
							print("UWAGA INDEX 'Z' PRZY KLASIE. IM KILLING THE ALGORITHM !")
							break;
						nazwaNowejKlasy = current_user.username+klasa[0][0]+letter
						query = "CREATE TABLE IF NOT EXISTS "+nazwaNowejKlasy+" (id integer NOT NULL PRIMARY KEY AUTOINCREMENT, Imię text, Nazwisko text , Kod_pocztowy text, Miejscowość text, Ulica text, Nr_budynku text, Nr_mieszkania text, Kod_pocztowy2 text, Miejscowość2 text, Ulica2 text, Nr_budynku2 text, Nr_mieszkania2 text, polski text, angielski text, niemiecki text, francuski text, wloski text, hiszpanski text,rosyjski text, matematyka text, fizyka text, informatyka text, historia text, biologia text, chemia text, geografia text, wos text, zajęcia_techniczne text, zajęcia_artstyczne text, edukacja_dla_bezpieczeństwa text, plastyka text, muzyka text, wf text, zachowanie text, klasa text,punkty text)"
						c.execute(query)
						conn.commit()
						while(inc2 < klasa[0][2] and j<len(uczniowie)):
							query = "INSERT INTO "+nazwaNowejKlasy+" ('Imię','Nazwisko','Kod_pocztowy','Miejscowość','Ulica','Nr_budynku','Nr_mieszkania','Kod_pocztowy2','Miejscowość2','Ulica2','Nr_budynku2','Nr_mieszkania2','polski','angielski','niemiecki','francuski','wloski','hiszpanski','rosyjski','matematyka','fizyka','informatyka','historia','biologia','chemia','geografia','wos','zajęcia_techniczne','zajęcia_artstyczne','edukacja_dla_bezpieczeństwa','plastyka','muzyka','wf','zachowanie','klasa','punkty') "
							query += "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
							c.execute(query,uczniowie[j][1:])
							c.execute("UPDATE uczniowie SET klasa=? WHERE id=?",(nazwaNowejKlasy,uczniowie[j][0]))
							conn.commit()
							j += 1
							inc2 += 1
						inc2 = 0
						inc += 1
						letter = ord(letter)
						letter += 1
						letter = chr(letter)

					c.execute("UPDATE klasy SET litera=\'"+letter+"\' WHERE id="+str(klasa[0][5]))
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
						"formFillClass":formFillClass,
					}

					return HttpResponseRedirect("/sms")

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
						"formFillClass":formFillClass,	
					}

					return HttpResponseRedirect("/sms")

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
						"formFillClass":formFillClass,
					}

					return HttpResponseRedirect("/sms")



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
				context={
						"current_user" : current_user,
						"formAddProfile":formAddProfile,
						"formAddStudent":formAddStudent,
						"formAddClass":formAddClass,
						"formAddAlgorithm":formAddAlgorithm,
						"formRemoveClass":formRemoveClass,
						"formRemoveProfile":formRemoveProfile,
						"formRemoveAlgorithm":formRemoveAlgorithm,
						"formFillClass":formFillClass,
					}

				return HttpResponseRedirect("/sms")

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
						"formFillClass":formFillClass,
					}
					return HttpResponseRedirect("/sms")

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
					context={
						"current_user" : current_user,
						"formAddProfile":formAddProfile,
						"formAddStudent":formAddStudent,
						"formAddClass":formAddClass,
						"formAddAlgorithm":formAddAlgorithm,
						"formRemoveClass":formRemoveClass,
						"formRemoveProfile":formRemoveProfile,
						"formRemoveAlgorithm":formRemoveAlgorithm,
						"formFillClass":formFillClass,
					}
					return HttpResponseRedirect("/sms")

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
						"formFillClass":formFillClass,			
					}

					return HttpResponseRedirect("/sms")

		context={
			"current_user" : current_user,
			"formAddProfile":formAddProfile,
			"formAddStudent":formAddStudent,
			"formAddClass":formAddClass,
			"formAddAlgorithm":formAddAlgorithm,
			"formRemoveClass":formRemoveClass,
			"formRemoveProfile":formRemoveProfile,
			"formRemoveAlgorithm":formRemoveAlgorithm,
			"formFillClass":formFillClass,	
		}
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
