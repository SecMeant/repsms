from django.contrib import admin
from .models import scSzkola
# Register your models here.
class scSzkolaAdmin(admin.ModelAdmin):
	fields=('nazwaSzkoly','email','telefon')
	class Meta:
		model=scSzkola
admin.site.register(scSzkola, scSzkolaAdmin)