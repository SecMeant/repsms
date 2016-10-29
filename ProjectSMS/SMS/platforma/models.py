from django.db import models
from datetime import timedelta , datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class accounts(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True)
	phoneNumber = models.IntegerField()
	created = models.DateTimeField(default=datetime.now())	
	expired = models.DateTimeField(default=datetime.now()+timedelta(days=1))	
	def __unicode__(self):
		return self.user.username

	def __str__(self):
		return self.user.username

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
# 	if created:
# 		accounts.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
# 	instance.accounts.save()