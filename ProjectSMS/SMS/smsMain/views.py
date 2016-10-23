from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction

# Create your views here.
@login_required
@transaction.atomic
def smsApp(request):
	
	if request.user.is_authenticated:
		current_user = request.user

		context={
			"current_user" : current_user,
		}
		return render (request, "SMS.html", context)