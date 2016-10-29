from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

class userAdmin(admin.ModelAdmin):
	model = User

admin.site.register(User,userAdmin)

