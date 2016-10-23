from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import logowanie , rejestracja , kontakt
from django.http import HttpResponseRedirect
import sqlite3
import os
 
# Create your views here.
def index(request):
	instanceLogowanie=logowanie()
	instanceRejestracja=rejestracja()
	instancekontakt=kontakt()
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	conn = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
	# instanceRejestracja = szkolaForm()
	if request.method == 'POST':
		if "zaloguj" in request.POST:
			pass
		elif "rejestracja" in request.POST:
			
			formRejestracja = rejestracja(request.POST)
			if formRejestracja.is_valid():
				subject = formRejestracja.cleaned_data['nazwaSzkoly']
				message = formRejestracja.cleaned_data['login']
				sender = formRejestracja.cleaned_data['haslo']
				cc_myself = formRejestracja.cleaned_data['email']
				c = conn.cursor()
				c.execute('CREATE TABLE IF NOT EXISTS stocks(date text, trans text, symbol text, qty real, price real)')
				c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
				conn.commit()
				conn.close()
				# instance = formRejestracja.save(commit=False)
				# instance.nazwaSzkoly = request.nazwaSzkoly
				# instance.save()
				context={
					"title":"SMS",
					"instanceL":instanceLogowanie,
					"instanceR":instanceRejestracja,
					"instanceC":instancekontakt,
					}
				return HttpResponseRedirect('/confirm')

	context={
		"title":"SMS",
		"instanceL":instanceLogowanie,
		"instanceR":instanceRejestracja,
		"instanceC":instancekontakt,
	}
	return render (request, "index.html", context)
def confirm(request):
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	conn = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
	c = conn.cursor()
	c.execute('SELECT * FROM stocks')
	print (c.fetchone())
	return render (request, "ConfirmRegister.html", {})