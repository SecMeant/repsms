from django.shortcuts import render
from .forms import szkolaForm,logowanie

 
# Create your views here.
def index(request):
	instanceLogowanie=logowanie()
	instanceRejestracja = szkolaForm()
	if request.method == 'POST':
		if "zaloguj" in request.POST:
			formLogowanie=szkolaForm(request.POST or None)
		else:
			
			formRejestracja = szkolaForm(request.POST or None)
			if formRejestracja.is_valid():
				instance = formRejestracja.save(commit=False)
				instance.nazwaSzkoly = request.nazwaSzkoly
				instance.save()
				return HttpResponseRedirect("")
	context={
		"title":"SMS",
		"instanceL":instanceLogowanie,
		"instanceR":instanceRejestracja,

	}
	return render (request, "manageindex.html", context)
