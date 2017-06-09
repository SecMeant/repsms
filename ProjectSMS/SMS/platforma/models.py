from django.db import models
from datetime import timedelta , datetime
from django.contrib.auth.models import PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
import pytz
import sqlite3,os

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)    
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(max_length=40, unique=True)
	nazwaSzkoly = models.CharField(max_length=100, blank=True)
	email = models.EmailField(blank=False,unique=True)
	password = models.CharField(max_length=256)
	phoneNumber = models.CharField(max_length=15)
	created = models.DateTimeField(default=datetime.now())	
	expired = models.DateTimeField(default=datetime.now()+timedelta(days=1))
	confirm = models.BooleanField(default=False)
	is_active = models.BooleanField(_('active'), default=True)
	is_staff = models.BooleanField(_('staff'), default=True)
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email', 'confirm', 'phoneNumber', 'nazwaSzkoly']

	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')

	def get_full_name(self):

		full_name = '%s %s' % (self.username, self.nazwaSzkoly)
		return full_name.strip()

	def get_short_name(self):

		return self.nazwaSzkoly

	def email_user(self, subject, message, from_email=None, **kwargs):

		send_mail(subject, message, from_email, [self.email], **kwargs)

	def natural_key(self):
		return (self.username, self.nazwaSzkoly)

	objects = UserManager()
	def is_expired(self):
		if self.expired < datetime.utcnow().replace(tzinfo=pytz.utc) and not self.is_superuser:
			BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			conn = sqlite3.connect(os.path.join(BASE_DIR,  'db.sqlite3'))
			c = conn.cursor()
			elo =c.execute("UPDATE platforma_user SET is_active=? WHERE email=?",(False,self.email))
			conn.commit()
			conn.close()
			return True

		return False
		