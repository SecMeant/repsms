from django.shortcuts import render
from .forms import logowanie , rejestracja, kontakt
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from .models import User
from django.contrib.auth import authenticate, login

def index(request):
	instanceLogowanie=logowanie()
	instanceRejestracja=rejestracja()	
	instancekontakt=kontakt()
	itemCarusel=['item','item active','item']
	if request.method == 'POST':
		instanceLogowanie=logowanie()
		if "zaloguj" in request.POST:
			varLog = logowanie(request.POST or None)
			if varLog.is_valid():
				passw = varLog.cleaned_data['haslo']
				loginU = varLog.cleaned_data['login']
				try:
					user = authenticate(username=loginU, password=passw)
				except:
					user=None
				if user is not None:
					login(request, user)
					return HttpResponseRedirect('/sms')
				else:
					return HttpResponseRedirect('#')

		elif "rejestracja" in request.POST:
			
			formRejestracja = rejestracja(request.POST or None)
			
			if formRejestracja.is_valid():
				
				formRejestracja.save()
				instanc = User.objects.get(username=formRejestracja.cleaned_data['username'])
				instanc.password=make_password(password=formRejestracja.cleaned_data['password'],
														salt=None,
														hasher='pbkdf2_sha1')
				instanc.save()
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

