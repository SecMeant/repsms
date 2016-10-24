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
				try:
					userLoginData =accounts.objects.get(login=login,password=passw)
				except accounts.DoesNotExist:
					userLoginData = None

				print(userLoginData.columns)
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

