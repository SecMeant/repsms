from django import forms
from .models import scSzkola

class szkolaForm(forms.ModelForm):
    class Meta:
        model = scSzkola
        fields = [
            "nazwaSzkoly",
            "email",
            "telefon",
		]
class logowanie(forms.Form):
	haslo=forms.CharField(label='haslo', max_length=100,widget=forms.PasswordInput(
		attrs={
		'type':"text", 
		'class':"form-control",
		'id':"psw", 
		'placeholder':"Wpisz haslo"})
		
	)
	login=forms.CharField(label='login', max_length=100,
		widget=forms.TextInput(
			attrs={
			'type':"text", 
			'class':"form-control",
			'id':"username", 
			'placeholder':"Wpisz login"})
		
	)
