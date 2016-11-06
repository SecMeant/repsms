from django.shortcuts import render
from .forms import logowanie , rejestracja, kontakt
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.hashers import make_password
from .models import User
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import string
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os, urllib
def RandomString(size = 8, chars=string.ascii_letters + string.digits):
	return ''.join(random.SystemRandom().choice(chars) for i in range(size))
			
def index(request):
	
	instanceLogowanie=logowanie()
	instanceRejestracja=rejestracja(initial=request.POST)
	instancekontakt=kontakt()
	passwordError={"login":False,"email":False,"passwordConfirm":False,"phoneNumber":False,}
	itemCarusel=['item','item active','item']
	if request.method == 'POST':
		instanceLogowanie=logowanie()
		if "zaloguj" in request.POST:
			instanceLogowanie = logowanie(request.POST or None)
			if instanceLogowanie.is_valid():

				passw = instanceLogowanie.cleaned_data['haslo']
				loginU = instanceLogowanie.cleaned_data['login']
				try:
					user = authenticate(username=loginU, password=passw)
				except:
					user=None
				if user is not None:
					login(request, user)
					return HttpResponseRedirect('/sms')
				else:
					return HttpResponse().__setitem__('instanceL',instanceLogowanie)

		elif "rejestracja" in request.POST:
			
			instanceRejestracja = rejestracja(request.POST or None)
			if instanceRejestracja.is_valid():
				if instanceRejestracja.cleaned_data['password']==instanceRejestracja.cleaned_data['passwordConfirm']:
					instanceRejestracja.save()
					instanc = User.objects.get(username=instanceRejestracja.cleaned_data['username'])
					instanc.password=make_password(password=instanceRejestracja.cleaned_data['password'],
														salt=None,
														hasher='pbkdf2_sha1')					
					instanc.save()
				else:
					itemCarusel=['item active','item','item']
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
	 }
	return render (request, "index.html", context)


def confirm(request):
	return render (request, "ConfirmRegister.html", {})

def remember(request):
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	BASE_DIR.join('templates/emailpassword')
	email=request.GET['email']
	email = urllib.parse.unquote(email)
	print(email)
	try:

		instance =User.objects.get(email=email)
		
		securePassword=RandomString();

		# try:
		# 	User.objects.get(password=securePassword)
		# except:
		# 	securePassword=RandomString();
		instance.password=make_password(password=securePassword,
														salt=None,
														hasher='pbkdf2_sha1')					
		instanc.save()
		me = "sagan.pawel1000@gmail.com"
		you = email
		msg = MIMEMultipart('alternative')
		msg['Subject'] = 'SMS przypomnienie hasła'
		msg['From'] = me
		msg['To'] = you
		text = "Email ten został wysłany w związku z rządaniem przypomnienia hasła dla konta %s. \n "  % instance.login
		text.join("Twoje nowe hasło to %s" % securePassword)
		fp = open(BASE_DIR, 'rb')
		# Create a text/plain message
		html = MIMEText(fp.read(),'html')
		fp.close()

		part1 = MIMEText(text, 'plain')
		part2 = MIMEText(html, 'html')

		msg.attach(part1)
		msg.attach(part2)

		s = smtplib.SMTP('smtp.gmail.com')
		s.sendmail(me, you, msg.as_string())
		s.quit()
	except:
		pass
	return HttpResponseRedirect('')