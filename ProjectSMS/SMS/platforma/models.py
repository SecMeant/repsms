from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class scSzkola(models.Model):
	nazwaSzkoly = models.CharField(max_length=30)
	email = models.EmailField(max_length=254)
	telefon = PhoneNumberField()
	def __str__(self):
		return str(self.phone_number)
class PhoneNumber:
	def __init__(self, country_code=None, region_code=None, phone_number=None):
		"""
		:type country_code: str
		:type region_code: str
		:type phone_number: str
		"""
		self.country_code = country_code
		self.google_phone_number = None
		self.region_code = region_code
		self.phone_number = phone_number