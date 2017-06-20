from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import addStudent, profilAndChoice, sortowanie
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import sqlite3,os
from smsMain import csvfuncs, funkcjeopty
from math import floor 
from .funcSort import SortPolishString
# Create your views here.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

@login_required
def main(request):
	
	if request.user.is_authenticated:

		if  request.user.is_expired():
			print(request.user.is_active)
			logout(request)
			HttpResponseRedirect('/')
		#obiekty formularzy
		Student = addStudent()
		Profil_ins = profilAndChoice()
		currentUser = request.user.username
		conn = sqlite3.connect(os.path.join(BASE_DIR+"\\SimpleData",currentUser +'.db'))
		c = conn.cursor()
		c.execute('CREATE TABLE IF NOT EXISTS "profile"( id integer , nazwa_profilu text, formatowanie text, table_labels)')
		
		c.execute('CREATE TABLE IF NOT EXISTS algorytm (id integer  NOT NULL PRIMARY KEY AUTOINCREMENT, polski integer,   angielski integer,   niemiecki integer,   francuski integer,   wloski integer,   hiszpanski integer,   rosyjski integer,   matematyka integer,   fizyka integer,   informatyka integer,   historia integer,   biologia integer,   chemia integer,   geografia integer,   wos integer,   zajęcia_techniczne integer,   zajęcia_artystyczne integer,   edukacja_dla_bezpieczeństwa integer,   plastyka integer,   muzyka integer,   wf integer,   religia integer,   zachowanie integer, Wynik_egzaminu_gimnazjalnego_z_języka_polskiego integer,   Wynik_egzaminu_gimnazjalnego_z_matematyki integer,   Wynik_egzaminu_gimnazjalnego_z_historii_i_wosu integer,   Wynik_egzaminu_gimnazjalnego_z_przedmiotów_przyrodniczych integer,   poziomie_podstawowym integer,   Wynik_egzaminu_gimnazjalnego_z_języka_obcego_na_poziomie_rozszerzonym integer)')
		
		if "importFile" in request.POST:
			
			userConfInstance =  profilAndChoice(request.POST or None,request.FILES,initial=request.POST)
			if userConfInstance.is_valid():
				profName = cleanString(userConfInstance.cleaned_data['profil'])
				subName = userConfInstance.cleaned_data['copystuff'].split(",")
				classSize = cleanString(userConfInstance.cleaned_data['wielkosc'])
				fileName = request.FILES['studentFile']
				sign_ask = "?" * (len(subName)+1)
				# querry prepare first set name id's of column, then amount of sign '?', finally all values
				querryPreparation =[ "(id, " + ",".join(subName).replace(' ','_') + ")", "(" + ",".join(sign_ask) + ")" ,tuple([None] +list( i+1 for i in reversed(range(len(subName)))))  ]
				# format query to appropriate string
				querry = 'INSERT INTO algorytm {} VALUES {}'.format(querryPreparation[0],querryPreparation[1])
				
				c.execute(querry,querryPreparation[2])
				last_insterted =c.execute('SELECT last_insert_rowid()');
				last_insterted_id =last_insterted.fetchone()[0]
				
				# make class sorted and divided
				makeClass(fileName,conn,profName,subName,classSize,last_insterted_id,userConfInstance.cleaned_data['stala_wielkosc'])
				conn.commit


				

			
		
		all_prof = c.execute("SELECT * FROM profile")
		drukuj_profile = all_prof.fetchall()
		
		drukuj_profile = [x[1] for x in drukuj_profile] # to get every second element inside list of tuples

				

		context={
		"formAddStudent" : Student,
		"formProfil":Profil_ins,
		"proflie_druk" : drukuj_profile,
		}
		conn.close()
		return render(request,"SMS_Simple.html",context)
	#HttpResponseRedirect('/')



def renderclass(request, classPro):
	if request.user.is_authenticated:
		if  request.user.is_expired():
			print(request.user.is_active)
			logout(request)
			HttpResponseRedirect('/')
		currentUser = request.user.username
		Profil_ins = profilAndChoice()
		sortuj_po = sortowanie()
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

		conn = sqlite3.connect(os.path.join(BASE_DIR+"\\SimpleData",currentUser +'.db'))
		c = conn.cursor()
		
		query = "SELECT * FROM " + classPro +" ORDER BY klasa_label"
		all_students= c.execute(query).fetchall()
		headerTable = [description[0] for description in c.description]

		zgrupowane_klasy = []
		subclass = []
		letters=[]
		for i, student in enumerate(all_students):
			if i == 0:
				subclass.append(student)
			else:
				if i == len(all_students)-1:
					letters.append(subclass[0][-1])
					subclass.append(student)
					zgrupowane_klasy.append(subclass)

				elif student[-1] == subclass[0][-1]  :
					subclass.append(student)
					
				else:
					letters.append(subclass[0][-1])
					zgrupowane_klasy.append(subclass)
					subclass = []
					subclass.append(student)

		
		# modify the labels set table
		if request.method == "POST":
			if "modify_labels_table" in request.POST:
				headers = request.POST['copystuff']
				
				c.execute("UPDATE profile SET table_labels = (?) WHERE nazwa_profilu = (?)",(headers,classPro))
				conn.commit();


	# Domyślnie nie sortujemy
		sort_id = 0
		
		if request.method == "GET":
			if 'kategoria' in request.GET:
				try:
					sortuj_po = sortowanie(initial = request.GET)
					sort_parametr = request.GET['kategoria']
					
			# id kolumny po ktorej posortujemy ucnziow	
					sort_id = headerTable.index(sort_parametr)
					print(sort_id)
				except :
					sort_id= 0
		if sort_id != 0 :
			i=0

			while (i < len(zgrupowane_klasy)):
				zgrupowane_klasy[i] = SortPolishString(zgrupowane_klasy[i],sort_id)
				i += 1

		# pull labels display
		column_label = c.execute("SELECT table_labels FROM profile WHERE nazwa_profilu = (?)", (classPro,) ).fetchone()[0]
		column_label = column_label.split(",")
		headerIdx = [headerTable.index(idx) for idx in column_label ]
		print(headerIdx)
		page_url = "/sms/simple/"+classPro
		page_url_edit = "/sms/simple/edit/"+classPro
		
		
		context={
			"formProfil":Profil_ins,
			"allStudents":zgrupowane_klasy,
			"sortowanie" : sortuj_po,
			"headerTable":column_label,
			"headerIdx":headerIdx,
			"headerOption":headerTable,
			"litery":letters,
			"page_url":page_url,
			"page_url_edit":page_url_edit,
		}
		return render (request, "printStudents.html",context)
		
def editclass(request, class_name):
	context ={

	}
	return render (request, "printStudents.html",context)

def cleanString(strr):

	new_str=""
	for c in strr:
		if 33 <= ord(c) <= 47 or 58 <= ord(c) <= 64:
			new_str+="_"
		else:
			new_str+=c

	return new_str

def makeClass(fileName,conn,profName,algo,classSize,last_insterted_id, size_mode):
	answer = []
	c = conn.cursor()
	
	for word in wantedtable:
		temp = csvfuncs.searchcsv(word,fileName)
		if(temp != None):
			answer.append(csvfuncs.searchcsv(word,fileName))
		else:
			answer.append('')
	
	csvfuncs.importcsv(wantedtable,answer,fileName,c,profName,"Pawel")

	
	divideClass(conn,profName,algo,classSize,last_insterted_id,size_mode)

	idClass = c.execute("SELECT id FROM profile WHERE nazwa_profilu = (?)",(profName,)).fetchone()[0]
	
	
					
	label = [ l +" DESC" for l in algo]
	c.execute("SELECT * FROM " + "t" + profName + " ORDER BY " + ",".join(label))
	allStudents = c.fetchall()
	
	formatowanie = c.execute("SELECT formatowanie FROM profile WHERE id =?",(idClass,)).fetchone()[0]
	
	formatowanie = formatowanie.split(',')
	base_ptr=[]
	top_ptr =[]
	for i,element in enumerate(formatowanie):
		if element is '': continue
		if i == 0:
			top_ptr.append(int(element))
			base_ptr.append(0)
		else:
			
			top_ptr.append(int(element) + int(top_ptr[i-1]))
			base_ptr.append(top_ptr[i-1])

	letters = ['A']
	for i in range(len(formatowanie)-1):
		letters.append(chr(ord(letters[i]) + 1) )

	# tworzenie listy tuple'ow wraz z iloscia uczniow kazdej klasy potrzebnych do odpowiedniego pogrupowania klas
	formatowanie=[(base,top)for base,top in zip(base_ptr,top_ptr)]
	# grupowanie klas  na podstawie formatowania
	zgrupowane_klasy = [[allStudents[i]for i in range(formatowanie[j][0],formatowanie[j][1])] for j in range(len(formatowanie)) ]
	# przypisanie lietrki kazdemu uczniowi
	for i , klasa in enumerate(zgrupowane_klasy):
		tmp_klasa = []
		for uczen in klasa:
			uczen = list(uczen)
			uczen.append(letters[i])
			del uczen[0]
			tmp_klasa.append(uczen)
		zgrupowane_klasy[i] = tmp_klasa


	colms =wantedtable
	
	colms.append("klasa_label")
	for i , klasa in enumerate(zgrupowane_klasy):
		for uczen in klasa:
			query = csvfuncs.generateQuery(profName,colms,len(colms),"INSERT INTO")
			
			c.execute(query, uczen)
	c.execute("DROP TABLE t"+profName)		
	conn.commit()




def divideClass(conn,profName,algo,classSize,last_insterted_id, size_mode):
	# insert rest of data to table after determine best class size
	c = conn.cursor()
	odp = []
	odpowiedzi = []
	strf="";
	ilosc = c.execute("SELECT COUNT(id) FROM {}".format("t"+profName)).fetchone()[0]

	if not size_mode:
	
		odpowiedzi.append(funkcjeopty.dejnumer(ilosc,int(classSize)))
		odp.append(funkcjeopty.optymalizuj(odpowiedzi[0],int(classSize)))
		odp[0] = funkcjeopty.rest(odp[0])
		for s in odp[0]:
			strf+=str(s)+","
	else:
		klasy = floor(ilosc/int(classSize))
		
		reszta = str(ilosc - int(classSize) * klasy)
		classSize += ","
		strf = (classSize) * klasy;
		strf += reszta
	table_labels = [
		"Imię", #1
		"Nazwisko",#2
		"Kod_pocztowy",#3
		"Miejscowość",#4
		"Ulica",#5
		"Nr_budynku",#6
		"Nr_mieszkania",#7
	]
	table_labels += algo;
	rawTable = ","
	rawTable = rawTable.join(table_labels)
	c.execute('INSERT INTO profile VALUES(?,?,?,?)',(last_insterted_id, profName, strf, rawTable))		
	conn.commit()

	