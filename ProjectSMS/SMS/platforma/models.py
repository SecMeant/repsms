from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings
from django import forms
from datetime import timedelta , datetime
from django.utils import timezone


# Create your models here.
class accounts(models.Model):
	username = models.CharField(max_length=60)
	login = models.CharField(max_length=60 ,unique=True)
	password = models.CharField(max_length=30)
	email = models.EmailField(max_length=50)
	phoneNumber = models.IntegerField()
	created = models.DateTimeField(default=datetime.now())	
	expired = models.DateTimeField(default=datetime.now()+timedelta(days=1))	
	def __unicode__(self):
		return self.username

	def __str__(self):
		return self.username
