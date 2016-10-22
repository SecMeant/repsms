from django.db import models

# Create your models here.

class klasa(models.Model):




class profile(models.Model):
	name = models.CharField(max_length=20)
	shortName = models.CharField(max_length=8)