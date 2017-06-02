from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import addStudent, profilAndChoice
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import sqlite3,os
from smsMain import csvfuncs, funkcjeopty
# Create your views here.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@login_required
def main(request):
	print(BASE_DIR)
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
		c.execute('CREATE TABLE IF NOT EXISTS "profile"( id integer , nazwa_profilu text,wielkosc_klasy integer)')
		
		c.execute('CREATE TABLE IF NOT EXISTS algorytm (id integer  NOT NULL PRIMARY KEY AUTOINCREMENT, polski integer,   angielski integer,   niemiecki integer,   francuski integer,   wloski integer,   hiszpanski integer,   rosyjski integer,   matematyka integer,   fizyka integer,   informatyka integer,   historia integer,   biologia integer,   chemia integer,   geografia integer,   wos integer,   zajęcia_techniczne integer,   zajęcia_artystyczne integer,   edukacja_dla_bezpieczeństwa integer,   plastyka integer,   muzyka integer,   wf integer,   religia integer,   zachowanie integer, Wynik_egzaminu_gimnazjalnego_z_języka_polskiego integer,   Wynik_egzaminu_gimnazjalnego_z_matematyki integer,   Wynik_egzaminu_gimnazjalnego_z_historii_i_wosu integer,   Wynik_egzaminu_gimnazjalnego_z_przedmiotów_przyrodniczych integer,   poziomie_podstawowym integer,   Wynik_egzaminu_gimnazjalnego_z_języka_obcego_na_poziomie_rozszerzonym integer)')
		
		if "importFile" in request.POST:
			
			userConfInstance =  profilAndChoice(request.POST or None,request.FILES,initial=request.POST)
			if userConfInstance.is_valid():
				profName = cleanString(userConfInstance.cleaned_data['profil'])
				subName = userConfInstance.cleaned_data['CopySubjects'].split(",")
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
				
				# conn.commit();
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
				

				for word in wantedtable:
					temp = csvfuncs.searchcsv(word,fileName)
					if(temp != None):
						answer.append(csvfuncs.searchcsv(word,fileName))
					else:
						answer.append('')

					print(answer)
				
				csvfuncs.importcsv(wantedtable,answer,fileName,c,profName)

				conn.commit()
			
			# insert rest of data to table after determine best class size
			odp = []
			odpowiedzi = []
			ilosc = c.execute("SELECT COUNT(id) FROM ?",(profName,)).fetchone()[0]
			if not userConfInstance.cleaned_data['stala_wielkosc']:
				
				odpowiedzi.append(funkcjeopty.dejnumer(ilosc,int(classSize)))
				odp.append(funkcjeopty.optymalizuj(odpowiedzi[0],int(classSize)))
				odp[0] = rest(odp[0])
			else:
				odp.append(funkcjeopty.simpleodp(ilosc,int(classSize)))
				odpowiedzi.append(funkcjeopty.simpleodpowiedzi(ilosc,int(classSize)))
					
			c.execute('INSERT INTO profile VALUES(?,?,?)',(last_insterted_id, profName,classSize))

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

		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		conn = sqlite3.connect(os.path.join(BASE_DIR+"\\SimpleData",currentUser +'.db'))
		c = conn.cursor()
		idClass = c.execute("SELECT id FROM profile WHERE nazwa_profilu = (?)",(classPro,)).fetchone()[0]
		algo = list(c.execute("SELECT * FROM algorytm WHERE id = (?) ",(idClass,)).fetchall())
		table_info =  c.execute("PRAGMA table_info(algorytm)").fetchall()
		column_name=[]
		# get column_names
		for item in table_info:
			column_name.append(item[1])
		# prepare data to make query which will choose students in right order 
		order_stuff =[]

		for i,item in enumerate(algo[0]):
			if item is not None and column_name[i] !="id":
				# until value is biger search index
				check_sec_sort=True
				if len(order_stuff) == 0:
					order_stuff.append((column_name[i],item))

				else:
					for k in range(len(order_stuff)):
						if order_stuff[k][1] > item:
							continue
						order_stuff.insert(k,(column_name[i],item))
						check_sec_sort=False
						break
					if check_sec_sort ==True:
						order_stuff.append((column_name[i],item))
						
		
		label = [ l[0] for l in order_stuff]
		c.execute("SELECT * FROM " + classPro + " ORDER BY " + ",".join(label))
		allStudents = c.fetchall()
		headerTable = [description[0] for description in c.description]

		context={
			"allStudents":allStudents,
			"headerTable":headerTable,
		}
		return render (request, "allStudents.html",context)

def cleanString(strr):
	new_str=""
	for c in strr:
		if 33 <= ord(c) <= 47 or 58 <= ord(c) <= 64:
			new_str+="_"
		else:
			new_str+=c

	return new_str
