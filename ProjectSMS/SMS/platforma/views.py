from django.shortcuts import render, redirect
from .forms import logowanie , rejestracja, kontakt , ChangePassword
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.hashers import make_password
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import ugettext_lazy as _
import string, random, sqlite3, smtplib,  os, urllib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import timedelta , datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def RandomString(size = 8, chars=string.ascii_letters + string.digits):
	return ''.join(random.SystemRandom().choice(chars) for i in range(size))
			
def index(request,typeMethod=None,activeid=None):
	# zmienna wyswietlajaca komunikat inforujacy o pomyslnej rejestraci i wysylajkaca email
	isregister=False
	# zmienna gotowy do logowania
	isReady=False
	# zmienna aktywujaca modal do zmiany hasla 
	isAboutToChangePass=False
	# Tworznie formularzy
	# Potwierzdzenie rejestracji  lub zmiana hasła
	if typeMethod == "activate":
		if(activeid !=None):
			try:
				conn = sqlite3.connect(os.path.join(BASE_DIR+"\\TempDB",'TemporaryUser.db'))
				c= conn.cursor()
				c.execute('SELECT * FROM tempUsers WHERE activCode=(?) ' ,[activeid])
				Users = c.fetchall()

				if(len(Users) == 1 ):
					
					User.objects._create_user(username=Users[0][0],
										 nazwaSzkoly=Users[0][1],
		                                 email=Users[0][2],
		                                 password=Users[0][3],
		                                 phoneNumber=Users[0][4],
		                                 )
					c.execute('DELETE FROM tempUsers WHERE activCode=(?) ' ,[activeid])

				conn.commit()
				conn.close()
				# Tworzenie potzrebnych tabel
				
				conn = sqlite3.connect(os.path.join(BASE_DIR+"\\userData", Users[0][0] + '.sqlite3'))

				c= conn.cursor()
				c.execute('CREATE TABLE IF NOT EXISTS "algorytmy" ( id integer NOT NULL PRIMARY KEY AUTOINCREMENT, nazwa text, jpolski integer, matematyka integer, jangielski integer, jniemiecki integer )')
				c.execute('CREATE TABLE IF NOT EXISTS "profile" ( shortname text, fullname text )')
				c.execute("CREATE TABLE IF NOT EXISTS klasy(nazwaKlasy text NOT NULL, profil text NOT NULL, liczebnosc integer NOT NULL, algorytm integer NOT NULL,litera text NOT NULL, id integer NOT NULL PRIMARY KEY AUTOINCREMENT )")
				c.execute("CREATE TABLE IF NOT EXISTS uczniowie(id integer NOT NULL PRIMARY KEY AUTOINCREMENT, Imię text, Nazwisko text , Kod_pocztowy text, Miejscowość text, Ulica text, Nr_budynku text, Nr_mieszkania text, Kod_pocztowy2 text, Miejscowość2 text, Ulica2 text, Nr_budynku2 text, Nr_mieszkania2 text, polski text, angielski text, niemiecki text, francuski text, wloski text, hiszpanski text,rosyjski text, matematyka text, fizyka text, informatyka text, historia text, biologia text, chemia text, geografia text, wos text, zajęcia_techniczne text, zajęcia_artstyczne text, edukacja_dla_bezpieczeństwa text, plastyka text, muzyka text, wf text, zachowanie text, klasa text)")
				conn.commit()
				conn.close()
				isReady=True
			except:
				raise Http404("Coś poszło nie tak !!")

			# return redirect('/',isReady=True)
	elif typeMethod == "changepassword":
		isAboutToChangePass=True

	# obsluzenie requestu zmiany hasła 
	if "changepass" in request.POST:
		instance = ChangePassword(request.POST or None,initial=request.POST)
		if instance.is_valid():
			key = instance.cleaned_data['superKey']
			password = instance.cleaned_data['password']
			conn=sqlite3.connect(os.path.join(BASE_DIR+"\\TempDB","UserTempChangePassword.db"))
			c = conn.cursor()
			c.execute("SELECT email FROM User WHERE key =?", [key])
			row = c.fetchall()
			email = row[0]
			obj = User.objects.get(email = email[0])#User.objects.get(email=email)
			obj.password=make_password(password=password,
													salt=None,
													hasher='pbkdf2_sha1')
			c.execute("DELETE FROM User Where email =?",[email[0]])
			conn.commit()
			conn.close()
			obj.save()
			isReady=True
		else:
			isAboutToChangePass=True


	# formluarz logowania
	instanceLogowanie=logowanie()
	# formularz rejestracji
	instanceRejestracja=rejestracja(initial=request.POST)
	# formularz zmiany hasla 
	instanceChangePass=ChangePassword()
	# Jesli jest zalogowany to wpisz do kontaktu jego email
	if(request.user.is_authenticated):
		instancekontakt=kontakt(initial={'email': request.user.email})
	else:
		instancekontakt=kontakt()

	# itemcarusel to zmeinna trzymajaca stan głownej karuzeli w razie wystapienia erroru
	itemCarusel=['item','item active','item']
	if request.method == 'POST':
		instanceLogowanie=logowanie()

		if "zaloguj" in request.POST:
			instanceLogowanie = logowanie(request.POST or None)
			if instanceLogowanie.is_valid():
				passw = instanceLogowanie.cleaned_data['haslo']
				loginU = instanceLogowanie.cleaned_data['login']
				 
			
				login(request,instanceLogowanie.userr)
				return HttpResponseRedirect('/version')
			else:
				isReady=True

		elif "rejestracja" in request.POST:
			instanceRejestracja = rejestracja(request.POST or None)
			if instanceRejestracja.is_valid():

				preRegister(instanceRejestracja);
				isregister=True
			else:	
				itemCarusel=['item active','item','item']
			
		elif "kontakt" in request.POST:
			instancekontakt= kontakt(request.POST or None,initial=request.POST)
			if instancekontakt.is_valid():
				imie = instancekontakt.cleaned_data['imie']
				nazwisko = instancekontakt.cleaned_data['nazwisko']
				email = instancekontakt.cleaned_data['email']
				tresc = instancekontakt.cleaned_data['tresc']
				if imie == "" and nazwisko == "":
					title="Anonymous"
				else:
					title = imie +' ' + nazwisko
				SendEmail('sagan.pawel1000@gmail.com',email,title,plain=tresc, html=None)

			itemCarusel=['item','item','item active']


			
	context={
		"title":"SMS",
		"instanceL":instanceLogowanie,
		"instanceR":instanceRejestracja,
		"instanceC":instancekontakt,
		"incanceP":instanceChangePass,
		"itemCarusel":itemCarusel,
		"isregister":isregister,
		"isChangePassword":isAboutToChangePass,
		"isReady":isReady,
	 }
	return render (request, "index.html", context)



def confirm(request):
	return render (request, "ConfirmRegister.html", {})

def remember(request):
	
	email=request.GET['email']
	email = urllib.parse.unquote(email)
	try:
		instance =User.objects.get(email=email)
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		conn=sqlite3.connect(os.path.join(BASE_DIR+"\\TempDB","UserTempChangePassword.db"))
		c=conn.cursor();
		c.execute("CREATE TABLE IF NOT EXISTS User(email text, key text)")
		while True:
			key=RandomString(size=32)
			c.execute('SELECT * FROM User WHERE key=(?) ' ,[key])
			if len(c.fetchall()) is 0:
				break
		c.execute("DELETE FROM User WHERE email=?",[email])
		c.execute("INSERT INTO User('email','key') VALUES(?,?)",(email,key))
		conn.commit()
		conn.close()
		# base data to send email  in my own email sender fun
		me = "sagan.pawel1000@gmail.com"
		you = email
		src='\\templates\emailpassword.html'
		title='SMS przypomnienie hasła'
		BASE_DIR+=src
		content = open(BASE_DIR, 'r',encoding="utf-8").read()
		content = content.replace("**user**",instance.username)
		content = content.replace("**pass**",key)
		SendEmail(me,you,title,plain=None,html=content)
	except:
		pass
	return HttpResponseRedirect('/')
def OWnLogout(request):
	logout(request)
	return HttpResponseRedirect('/')

def SendEmail(me,you,title, **kwargs):
	
	msg = MIMEMultipart('alternative')
	msg['Subject'] = title
	msg['From'] = me
	msg['To'] = you
	msg['Content-Type'] = "text/html; charset=utf-8"

	if kwargs['plain'] is not None:
		part1 = MIMEText(kwargs['plain'], 'plain',"utf-8")
		msg.attach(part1)
	if kwargs['html'] is not None:	
		part2 = MIMEText(kwargs['html'].encode('utf-8'), 'html', 'utf-8')
		
		msg.attach(part2)
	login="sagan.pawel1000@gmail.com"
	password="GHDR22I.P!S"
	s = smtplib.SMTP('smtp.gmail.com:587')
	s.ehlo()
	s.starttls()
	s.login(login,password)
	s.sendmail(me, you, msg.as_string())
	s.quit()

def preRegister(Data):
	# create db if not exist
	
	conn = sqlite3.connect(os.path.join(BASE_DIR+"\\TempDB",'TemporaryUser.db'))
	tUser = conn.cursor()
	tUser.execute("CREATE TABLE IF NOT EXISTS tempUsers(username text, nazwaSzkoly text, email text, password text ,phoneNumber integer,created timestamp, activCode text,expired timestamp)")

	username=Data.cleaned_data['username']
	nazwaSzkoly=Data.cleaned_data['nazwaSzkoly']
	email=Data.cleaned_data['email']
	password=Data.cleaned_data['password']
	phoneNumber=Data.cleaned_data['phoneNumber']
	created=datetime.now()

	while True:
		activateCode=RandomString(size=32)
		tUser.execute('SELECT * FROM tempUsers WHERE activCode=(?) ' ,[activateCode])

		if len(tUser.fetchall()) is 0:
			break

	
	tUser.execute("INSERT INTO tempUsers ('username','nazwaSzkoly','email','password','phoneNumber','created','activCode','expired') VALUES(?,?,?,?,?,?,?,?)",
				(username,nazwaSzkoly,email,password,phoneNumber,created,activateCode,created + timedelta(days=1)))
	conn.commit()
	conn.close()
	me = "sagan.pawel1000@gmail.com"
	you = email
	src='\\templates\\rejestracja.html'
	title='Witamy w aplikacji SMS'
	content = open(BASE_DIR + src, 'r',encoding="utf-8").read()
	content = content.replace("**activ**",activateCode)

	SendEmail(me,you,title,plain=None,html=content)
def chooseVerion(request):
	return render(request, "choosePlatform.html")
