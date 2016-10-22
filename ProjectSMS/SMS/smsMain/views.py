from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from .forms import szkolaForm
from django.utils import timezone
# Create your views here.

def smsApp(request):
	if request.user.is_authenticated:
		current_user = request.user
		now=timezone.now();
		if request.method == 'POST':
			form=szkolaForm(request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/')
		else:
			form = szkolaForm()

		context={
			"current_user" : current_user,
			"curent_date": now,
			"form" : form,
		}
		return render (request, "SMS.html", context)
	else:
		raise Http404