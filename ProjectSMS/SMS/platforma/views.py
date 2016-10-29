from django.shortcuts import render
from .forms import logowanie , rejestracja ,rejestracjaExtends, kontakt
from django.http import HttpResponseRedirect
from .models import accounts
# Create your views here.
def index(request):
	# instanceRejestracja = szkolaForm()
	if request.method == 'POST':
		instanceLogowanie=logowanie()
		if "zaloguj" in request.POST:
			varLog = logowanie(request.POST or None,instance=request.user)
			if varLog.is_valid():
				passw = varLog.cleaned_data['haslo']
				login = varLog.cleaned_data['login']

				try:
					userLoginData =accounts.objects.get(login=login,password=passw)
				except accounts.DoesNotExist:
					userLoginData = None

				print(userLoginData)

		elif "rejestracja" in request.POST:
			formRejestracja = rejestracja(request.POST or None)
			formRejestracjaEx = rejestracjaExtends(request.POST or None)
			if formRejestracja.is_valid() and formRejestracjaEx.is_valid:
				formRejestracja.save()
				formRejestracjaEx.save()
				return HttpResponseRedirect('/confirm')

		elif "kontakt" in request.POST:
			pass	
	else:
		instanceLogowanie=logowanie()
		instanceRejestracja=rejestracja()
		instanceRejestracjaExtends = rejestracjaExtends()
		instancekontakt=kontakt()		
	context={
		"title":"SMS",
		"instanceL":instanceLogowanie,
		"instanceR":instanceRejestracja,
		"instanceReEx":instanceRejestracjaExtends,
		"instanceC":instancekontakt,
	}
	return render (request, "index.html", context)
def confirm(request):
	return render (request, "ConfirmRegister.html", {})

