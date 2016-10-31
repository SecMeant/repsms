from django.shortcuts import render
from .forms import logowanie , rejestracja, kontakt
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from .models import User
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
# def validate(postRepaired):
# 	errors={"login":False,"email":False,"passwordConfirm":False,"phoneNumber":False,}
# 	try:
# 		validate_email( postRepaired['email'] )
		

# 	except ValidationError:
# 		errors['email']="Nieprawidlowy email"
# 	try:

# 		postRepaired['phoneNumber']=str(postRepaired['phoneNumber']).replace("+", "")
# 		postRepaired['phoneNumber']=str(postRepaired['phoneNumber']).replace(" ", "")
# 		postRepaired['phoneNumber']=str(postRepaired['phoneNumber']).replace("(", "")
# 		postRepaired['phoneNumber']=str(postRepaired['phoneNumber']).replace(")", "")
# 		postRepaired['phoneNumber']=str(postRepaired['phoneNumber']).replace("-", "")
# 		if not len(str(postRepaired['phoneNumber'])) >=9 or not str(postRepaired['phoneNumber']).isdigit():
# 			raise TypeError
# 	except TypeError:
# 		errors['phoneNumber']="Nieprawidlowy numer telefonu"
	
# 	if postRepaired['password'] == postRepaired['passwordConfirm'] and len(postRepaired['password']) >0:
# 		pass
# 	else:
# 		errors['passwordConfirm']="Hasła się nie zgadzają"
	
# 	try: 
# 		User.objects.get(username=postRepaired['username'])
# 		errors['login']="Login jest juz zajety"
# 	except:
# 		pass				
# 	return postRepaired ,errors
			

def index(request):
	instanceLogowanie=logowanie()
	instanceRejestracja=rejestracja(initial=request.POST)
	instancekontakt=kontakt()
	passwordError={"login":False,"email":False,"passwordConfirm":False,"phoneNumber":False,}
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

