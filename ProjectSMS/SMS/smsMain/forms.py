from django import forms
from platforma.models import scSzkola

class szkolaForm(forms.ModelForm):
    class Meta:
        model = scSzkola
        fields = [
            "nazwaSzkoly",
            "email",
		]