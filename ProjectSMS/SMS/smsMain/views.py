from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import addProfile, addStudent, addClass, addAlgorithm, removeClass, removeProfile, removeAlgorithm, fillClass, formEditStudent
from .funkcjeopty import dejnumer, optymalizuj, rest
from .fillfuncs import fillclasses, fillclasses_sqlDict
from .vec import vectorContains, choiceFieldTupleContains
import os
import sqlite3
import math
from .csvfuncs import searchcsv, importcsv
from django.contrib.auth import logout
from operator import itemgetter
from .dbfuncs import sqlDict, sqlDict_sort

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
		# I want to leave a nice comment for line under for loop, becouse its a true beauty !
		# im iterating data in loop as usual, appending a ClassId just after casting to string from integer
		# than adding a '-' and concatenating name of the class to display it in a list, 
		# the class id is the value passed to remove method later
		# Im adding '-' because the name of class can contain spaces and im calling split() fucntion to
		# make this work like this [(a),(b)] - like multidimensinal array, because the choiceField function requires that
		# so by adding a dash im making sure that the split will happen just between right data.
		# After all im not sure of im doing this concatenate the right way, but im just a python begginer so..
		klasy = sqlDict(c, "SELECT * FROM klasy")
		klasypass = []
		#nk - name of class
		#idk - id of class
		for nk, idk in zip(klasy['nazwaKlasy'],klasy['id']):
			klasypass.append((str(idk)+"-"+nk).split("-"))

		#Im getting class names from db from every student
		#then every unique class is appended to klasyPostfix which will contain
		#list of all existing classes
		uczniowie = sqlDict(c, "SELECT * FROM uczniowie")
		klasyPostfix = []

		for klasa in uczniowie['klasa']:
			if( not( vectorContains(klasyPostfix,klasa) ) and klasa != None ):
				klasyPostfix.append(klasa)

		formAddProfile = addProfile
		formAddStudent = addStudent
		formAddAlgorithm = addAlgorithm
		formRemoveProfile = removeProfile(profile=(profiles))
		formAddClass = addClass(profile=(profiles),algorytm=(algorithmspass))
		formRemoveClass = removeClass(klasy=(klasypass))
		formRemoveAlgorithm = removeAlgorithm(algorytm=(algorithmspass))
		formFillClass = fillClass(klasy=(klasypass))

		#Gets the value of session variable that fillclass will set to 1 if overflow in class index occurs
		#So the value will be passed once to the jinja to display notification
		fillclassOF = request.session.get('SfillClassOF')
		request.session['SfillClassOF'] = 0

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
			"fillclassOF":fillclassOF,
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
					klasa = sqlDict(c, "SELECT * FROM klasy WHERE id=" + formFillClass.cleaned_data['klasy'])

					c.execute("SELECT * FROM uczniowie WHERE klasa IS NULL")

					uczniowie = c.fetchall()
					uczniowie = list(map(list,uczniowie))

					# start of implementation of opti functions from php
					ile = len(uczniowie)
					if(ile>=1 and sposob==True):
						odp = []
						odpowiedzi = [] # I have no idea why i chose similar names. Have no time to figure it out right now
						sizeofclass = int(klasa['liczebnosc'][0])
						odpowiedzi.append(dejnumer(ile,sizeofclass)) # First argument is size of all students to sort out, secound is size of class
						odp.append(optymalizuj(odpowiedzi[0],sizeofclass)) # Same arguments as above here
						odp[0] = rest(odp[0]) # Here as argument I need returned value from optymalizuj function
						uczniowie = sqlDict(c,"SELECT * FROM uczniowie WHERE klasa IS NULL")
						fillclassOF = fillclasses_sqlDict(c,conn,klasa,uczniowie,current_user,odp) #fillclasses_sqlDict returns 0 when no errors occur and 1 when index to class is above 'Z'

					else:
						uczniowie = sqlDict(c,"SELECT * FROM uczniowie WHERE klasa IS NULL")
						fillclassOF = fillclasses_sqlDict(c,conn,klasa,uczniowie,current_user,0) #fillclasses_sqlDict returns 0 when no errors occur and 1 when index to class is above 'Z'
					# end of implementation

					#setting the session variable to return value of fillclasses_sqlDict funtion
					#It will trigger the pop-up in jinja to display message to user that index in class have overflowed
					request.session['SfillClassOF'] = fillclassOF

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
					"Imię",
					"Pesel",
					"Nazwisko",
					"Kod pocztowy",
					"Miejscowość",
					"Ulica",
					"Nr budynku",
					"Nr mieszkania",
					"polski",
					"angielski",
					"niemiecki",
					"francuski",
					"wloski",
					"hiszpanski",
					"rosyjski",
					"matematyka",
					"fizyka",
					"informatyka",
					"historia",
					"biologia",
					"chemia",
					"geografia",
					"wos",
					"zajęcia techniczne",
					"zajęcia artstyczne",
					"edukacja dla bezpieczeństwa",
					"plastyka",
					"muzyka",
					"wf",
					"zachowanie",
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
		# so im just targeting it worth looking sometime when crash occurs.
		classes = []
		for each in classList:
			query = "SELECT * FROM uczniowie WHERE klasa='"+each+"'"
			c.execute(query)
			result = c.fetchall()
			if result:
				classes.append(result)

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

def manageStudents(request):

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

	return render(request, "manageStudent.html", context)

def deleteStudentsFromClass(request, id):
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

		query = "SELECT * FROM uczniowie WHERE id="+id
		uczen = sqlDict(c, query)
		


		if(len(uczen) != 1):
			print("Error when deleting student")
			return redirect(smsApp)

		klasa = uczen['klasa'][0]

		query = "DELETE FROM "+ klasa +" WHERE iducznia="+id #Usuwa ucznia z tabeli klasy do ktorej nalezy
		c.execute(query)
		conn.commit()

		query = "UPDATE uczniowie SET klasa = NULL WHERE id="+id #Usuwa wartosc z kolumny klasa usuniętgo ucznia
		c.execute(query)
		conn.commit()
		conn.close()

	return redirect(showSpecificClass, klasa)

def showSpecificClass(request, klasa):
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

		query = "SELECT * FROM uczniowie WHERE klasa='"+klasa+"'"
		c.execute(query)
		allStudents = c.fetchall()
		headerTable = [description[0] for description in c.description]

		headerWidth = len(headerTable) + 1

		context = {
			"allStudents":allStudents,
			"headerTable":headerTable,
			"headerWidth":headerWidth,
			"klasa":klasa,
		}

	return render(request, "studentsInClass.html" , context)

def editStudent(request,id):
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

		#Im getting class names from db from every student
		#then every unique class is appended to klasyPostfix which will contain
		#list of all existing classes
		query = "SELECT * FROM uczniowie"
		uczniowie = sqlDict(c, query)
		klasyPostfix = []
		klasyPostfix.append(("Brak","Brak"))

		for klasa in uczniowie['klasa']:
			if( not( choiceFieldTupleContains(klasyPostfix,klasa) ) and klasa != None ):
				klasyPostfix.append((klasa,klasa))

		# Edytowanie danych studenta klasy

		if "formEditStudent" in request.POST:
			EditStudent =  formEditStudent(request.POST,klasy=(klasyPostfix))
			if EditStudent.is_valid():
				imieUcznia = EditStudent.cleaned_data['imie']
				nazwiskoUcznia = EditStudent.cleaned_data['nazwisko']
				kod1Ucznia = EditStudent.cleaned_data['kod1']
				kod2Ucznia = EditStudent.cleaned_data['kod2']
				kodUcznia1 = kod1Ucznia +'-'+ kod2Ucznia
				miejscowoscUcznia = EditStudent.cleaned_data['miejscowosc']
				ulicaUcznia = EditStudent.cleaned_data['ulica']
				nrbudynkuUcznia = EditStudent.cleaned_data['nrbudynku']
				nrmieszkaniaUcznia = EditStudent.cleaned_data['nrmieszkania']
				kod12Ucznia = EditStudent.cleaned_data['kod12']
				kod22Ucznia = EditStudent.cleaned_data['kod22']
				kodUcznia2 = kod12Ucznia +'-'+ kod22Ucznia
				miejscowosc2Ucznia = EditStudent.cleaned_data['miejscowosc2']
				ulica2Ucznia = EditStudent.cleaned_data['ulica2']
				nrbudynku2Ucznia = EditStudent.cleaned_data['nrbudynku2']
				nrmieszkania2Ucznia = EditStudent.cleaned_data['nrmieszkania2']
				ocenaPolskiUcznia = EditStudent.cleaned_data['ocenPol']
				ocenaMatematykaUcznia = EditStudent.cleaned_data['ocenMat']
				ocenaAngielskiUcznia = EditStudent.cleaned_data['ocenAng']
				ocenaNiemieckiUcznia = EditStudent.cleaned_data['ocenNiem']
				klasaucznia = EditStudent.cleaned_data['klasa']	
				iducznia = EditStudent.cleaned_data['iducznia']


				query = "SELECT * FROM uczniowie WHERE id={}".format(id)
				uczen = sqlDict(c, query)

				if(len(uczen['id']) == 1):
					if(uczen['klasa'][0] != klasaucznia):
						klasaOld = uczen['klasa'][0]
						if(klasaOld != None and klasaOld != 'Brak'):
							c.execute("DELETE FROM {} WHERE iducznia={}".format(klasaOld,id))
							conn.commit()
						if(klasaucznia != None and klasaucznia != 'Brak'):
							query = "INSERT INTO {} (iducznia,Imię,Nazwisko) VALUES('{}','{}','{}')".format(klasaucznia,iducznia,imieUcznia,nazwiskoUcznia)
							c.execute(query)
							conn.commit()
				if(klasaucznia != None and klasaucznia != 'Brak'):
					query = "UPDATE uczniowie SET Imię='{}',Nazwisko='{}',Kod_pocztowy='{}',Miejscowość='{}',Ulica='{}',Nr_budynku='{}',Nr_mieszkania='{}',Kod_pocztowy2='{}',Miejscowość2='{}',Ulica2='{}',Nr_budynku2='{}',Nr_mieszkania2='{}',polski='{}',matematyka='{}',angielski='{}',niemiecki='{}',klasa='{}' WHERE id={}".format(imieUcznia,nazwiskoUcznia,kodUcznia1,miejscowoscUcznia,ulicaUcznia,nrbudynkuUcznia,nrmieszkaniaUcznia,kodUcznia2,miejscowosc2Ucznia,ulica2Ucznia,nrbudynku2Ucznia,nrmieszkania2Ucznia,ocenaMatematykaUcznia,ocenaPolskiUcznia,ocenaAngielskiUcznia,ocenaNiemieckiUcznia,klasaucznia,iducznia)
				else:
					query = "UPDATE uczniowie SET Imię='{}',Nazwisko='{}',Kod_pocztowy='{}',Miejscowość='{}',Ulica='{}',Nr_budynku='{}',Nr_mieszkania='{}',Kod_pocztowy2='{}',Miejscowość2='{}',Ulica2='{}',Nr_budynku2='{}',Nr_mieszkania2='{}',polski='{}',matematyka='{}',angielski='{}',niemiecki='{}',klasa=NULL WHERE id={}".format(imieUcznia,nazwiskoUcznia,kodUcznia1,miejscowoscUcznia,ulicaUcznia,nrbudynkuUcznia,nrmieszkaniaUcznia,kodUcznia2,miejscowosc2Ucznia,ulica2Ucznia,nrbudynku2Ucznia,nrmieszkania2Ucznia,ocenaMatematykaUcznia,ocenaPolskiUcznia,ocenaAngielskiUcznia,ocenaNiemieckiUcznia,iducznia)
				c.execute(query)
				conn.commit()
				
		query = "SELECT * FROM uczniowie WHERE id="+id
		student = sqlDict(c, query)

		try:
			kod = student['Kod_pocztowy'][0].split("-")
		except:
			kod = []
			kod.append(None)
			kod.append(None)
		try:
			kod2 = student['Kod_pocztowy2'][0].split("-")
		except:
			kod2 = []
			kod2.append(None)
			kod2.append(None)

		instanceEditStudent=formEditStudent(initial={
			'imie':student['Imię'][0],
			'nazwisko':student['Nazwisko'][0],
			'kod1':kod[0],
			'kod2':kod[1],
			'miejscowosc':student['Miejscowość'][0],
			'ulica':student['Ulica'][0],
			'nrbudynku':student['Nr_budynku'][0],
			'nrmieszkania':student['Nr_mieszkania'][0],
			'kod12':kod2[0],
			'kod22':kod2[1],
			'miejscowosc2':student['Miejscowość2'][0],
			'ulica2':student['Ulica2'][0],
			'nrbudynku2':student['Nr_budynku2'][0],
			'nrmieszkania2':student['Nr_mieszkania2'][0],
			'ocenPol':student['polski'][0],
			'ocenMat':student['matematyka'][0],
			'ocenAng':student['angielski'][0],
			'ocenNiem':student['niemiecki'][0],
			'klasa':student['klasa'][0],
			'iducznia':id
			},klasy=(klasyPostfix))

		context = {
			"formEditStudent":instanceEditStudent,
		}

		conn.close()

		return render(request, "editStudent.html" , context)
					
	return render(request, "editStudent.html" , context)