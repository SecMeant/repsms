from django.shortcuts import render
from .forms import logowanie , rejestracja, kontakt
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.hashers import make_password
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import ugettext_lazy as _
import string, random, sqlite3, smtplib,  os, urllib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def RandomString(size = 8, chars=string.ascii_letters + string.digits):
	return ''.join(random.SystemRandom().choice(chars) for i in range(size))
			
def index(request,activeid=None):
	# zmienna wyswietlajaca komunikat inforujacy o pomyslnej rejestraci i wysylajkaca email
	isregister=False
	# zmienna po wyslaniu emaila inforumjaca uzytkownia ze wszystko Ok
	isReady=False
	# Tworznie formularzy
	if(activeid !=None):
		conn = sqlite3.connect(os.path.join(BASE_DIR,'TemporaryUser.db'))
		c= conn.cursor()
		c.execute('SELECT * FROM tempUsers WHERE username=(?) ' ,['Test1'])
		Users = c.fetchall()
		print(len(Users))
		if(len(Users) != 1 ):
			print(activeid)
			User.objects.create_user(username=Users[0][0],
								 nazwaSzkoly=Users[0][1],
                                 email=Users[0][2],
                                 password=Users[0][3],
                                 phoneNumber=Users[0][4],
                                 )
			isReady=True;
		return HttpResponseRedirect('/')
		conn.close()

	instanceLogowanie=logowanie()
	instanceRejestracja=rejestracja(initial=request.POST)
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
				
				login(request, instanceLogowanie.userr)
				return HttpResponseRedirect('/sms')
			else:
				return HttpResponse().__setitem__('instanceL',instanceLogowanie)

		elif "rejestracja" in request.POST:
			instanceRejestracja = rejestracja(request.POST or None)
			if instanceRejestracja.is_valid():

				preRegister(instanceRejestracja);
				isregister=True
			else:	
				itemCarusel=['item active','item','item']
			
		elif "kontakt" in request.POST:
			itemCarusel=['item','item','item active']

			
	context={
		"title":"SMS",
		"instanceL":instanceLogowanie,
		"instanceR":instanceRejestracja,
		"instanceC":instancekontakt,
		"itemCarusel":itemCarusel,
		"isregister":isregister,
	 }
	return render (request, "index.html", context)


def confirm(request):
	return render (request, "ConfirmRegister.html", {})

def remember(request):
	
	email=request.GET['email']
	email = urllib.parse.unquote(email)
	try:

		instance =User.objects.get(email=email)
		
		securePassword=RandomString();

		while True:
			try:
				User.objects.get(password=securePassword)
				securePassword=RandomString()
			except:
				break
		
		instance.password=make_password(password=securePassword,
														salt=None,
														hasher='pbkdf2_sha1')					
		instance.save()
		# base data to send email  in my own email sender fun
		me = "sagan.pawel1000@gmail.com"
		you = email
		src='\\templates\emailpassword.html'
		title='SMS przypomnienie hasła'
		text = "Email ten został wysłany w związku z rządaniem przypomnienia hasła dla konta" +instance.username+"\n"
		text.join("Twoje nowe hasło to %s" % (securePassword,))
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		BASE_DIR+=src
		content = open(BASE_DIR, 'r').read()
		
		SendEmail(me,you,title,plain=text,html=content)
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
	print(msg.as_string())
	s.sendmail(me, you, msg.as_string())
	s.quit()

def preRegister(Data):
	# create db if not exist
	
	conn = sqlite3.connect(os.path.join(BASE_DIR,'TemporaryUser.db'))
	tUser = conn.cursor()
	tUser.execute("CREATE TABLE IF NOT EXISTS tempUsers(username text, nazwaSzkoly text, email text, password text ,phoneNumber integer,created timestamp, activCode text)")

	username=Data.cleaned_data['username']
	nazwaSzkoly=Data.cleaned_data['nazwaSzkoly']
	email=Data.cleaned_data['email']
	password=make_password(password=Data.cleaned_data['password'],
													salt=None,
													hasher='pbkdf2_sha1')
	phoneNumber=Data.cleaned_data['phoneNumber']
	created=datetime.now()

	while True:
		activateCode=RandomString(size=32)
		print(activateCode)
		tUser.execute('SELECT * FROM tempUsers WHERE activCode=(?) ' ,[activateCode])
		if tUser.rowcount == -1:
			break

	
	tUser.execute("INSERT INTO tempUsers ('username','nazwaSzkoly','email','password','phoneNumber','created','activCode') VALUES(?,?,?,?,?,?,?)",
				(username,nazwaSzkoly,email,password,phoneNumber,created,activateCode))
	conn.commit()
	conn.close()
	me = "sagan.pawel1000@gmail.com"
	you = 'pawel.sagan@op.pl'
	src='\\templates\\rejestracja.html'
	title='Witamy w aplikacji SMS'
	content = open(BASE_DIR + src, 'r').read()
	content = content.replace("**activ**",activateCode)

	SendEmail(me,you,title,plain=None,html=content)


