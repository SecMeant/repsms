from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# class csvImporter(models.Model):
# 	upload = models.FileField(upload_to='uploads/')