from django.contrib import admin
from .models import accounts
# Register your models here.
class userAdmin(admin.ModelAdmin):
	class Meta:
		model=accounts
	list_display = ["username", "login", "created"]	
admin.site.register(accounts, userAdmin)		