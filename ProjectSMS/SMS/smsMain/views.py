from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import addProfile
import os
import sqlite3

# Create your views here.
@login_required
@transaction.atomic
def smsApp(request):
	
	if request.user.is_authenticated:
		current_user = request.user

		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		dbname = current_user.username
		dbname += ".sqlite3"
		conn = sqlite3.connect(os.path.join(BASE_DIR, current_user.username + '.sqlite3'))
		formAddProfile = addProfile

		if request.method == 'POST':
			if "costaminnego" in request.POST:
				pass
			elif "addProfile" in request.POST:
				
				formAddProfile = addProfile(request.POST)
				if formAddProfile.is_valid():
					fullname = formAddProfile.cleaned_data['newProfileFullName']
					shortname = formAddProfile.cleaned_data['newProfileShortName']
					c = conn.cursor()
					c.execute("CREATE TABLE IF NOT EXISTS profile(fullname text, shortname text)")
					c.execute("SELECT * FROM profile")
					same = False
					for row in c.fetchall():
						if (row[0] == fullname or row[1] == shortname):
							same = True
							break
					if(same == False):
						c.execute("INSERT INTO profile VALUES(?,?)",(fullname,shortname))
					conn.commit()
					conn.close()
		context={
			"current_user" : current_user,
			"form":formAddProfile,
		}
		return render (request, "SMS.html", context)