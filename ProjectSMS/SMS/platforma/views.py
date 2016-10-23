from django.shortcuts import render
from .forms import logowanie , rejestracja , kontakt
from django.http import HttpResponseRedirect
import sqlite3
import os
from .models import accounts
from django.utils import timezone
# Create your views here.
def index(request):
	instanceLogowanie=logowanie()
	instanceRejestracja=rejestracja()
	instancekontakt=kontakt()

	# instanceRejestracja = szkolaForm()
	if request.method == 'POST':
		if "zaloguj" in request.POST:
			varLog = logowanie(request.POST or None)
			if varLog.is_valid():
				passw = varLog.cleaned_data['haslo']
				login = varLog.cleaned_data['login']
				
				User = accounts.objects.raw('SELECT login, password FROM platforma WHERE login=%s and password=%s',[login, passw])#all().filter(login=login)
				print(User)
				# if User.object. password is passw: 
				# print("%s , %s" %(login , passw)) 
				# for User in allUsers:
				# 	for login , haslo in (user.login , user.password):

		elif "rejestracja" in request.POST:
			
			formRejestracja = rejestracja(request.POST or None)
			if formRejestracja.is_valid():
				formRejestracja.save(commit=False)
				formRejestracja.created=timezone.now()
				formRejestracja.save()
				return HttpResponseRedirect('/confirm')
		elif "kontakt" in request.POST:
			pass		
	context={
		"title":"SMS",
		"instanceL":instanceLogowanie,
		"instanceR":instanceRejestracja,
		"instanceC":instancekontakt,
	}
	return render (request, "index.html", context)
def confirm(request):
	
	return render (request, "ConfirmRegister.html", {})