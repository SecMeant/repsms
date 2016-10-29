from django.contrib import admin
from .models import accounts
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

class AccountsInline(admin.StackedInline):
    model=accounts
    can_delete = False
    verbose_name_plural = 'accounts'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (AccountsInline, )

class Accounts(admin.ModelAdmin):
    model=accounts
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(accounts, Accounts)			