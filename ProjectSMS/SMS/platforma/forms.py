from django import forms
from .models import accounts
from django.forms import ModelForm
from django.contrib.auth.models import User
class logowanie(forms.Form):
	haslo=forms.CharField(label='haslo', max_length=100, widget=forms.PasswordInput(
		attrs={
		'type':"password", 
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
class rejestracja(ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'username', 'email','password')
		widgets = {
		'username': forms.TextInput(
			attrs={
			'type':"text", 
			'class':"form-control",
			'id':"email", 
			'placeholder':"Wpisz login"}),

		'first_name': forms.TextInput(
			attrs={
			'type':"text", 
			'class':"form-control",
			'id':"login", 
			'placeholder':"Wpisz nazwe szkoly"}),

		'password': forms.PasswordInput(
			attrs={
			'type':"password", 
			'class':"form-control",
			'id':"password", 
			'placeholder':"Wpisz hasło"}),

		'email': forms.TextInput(
			attrs={
			'type':"text", 
			'class':"form-control",
			'id':"email", 
			'placeholder':"Wpisz email"}),
		}
		labels = {
			'first_name': ('Nazwa Szkoły'),
			'username': ('Login'),
			'password': ('Hasło'),
			'email': ('E-mail'),
		}

class rejestracjaExtends(ModelForm):
	confirm=forms.BooleanField(label='Akceptacja regulaminu')
	class Meta:
		model=accounts
		fields=('phoneNumber',)
		widgets = {
		'phoneNumber': forms.TextInput(
			attrs={
			'type':"text", 
			'class':"form-control",
			'id':"phoneNumber", 
			'placeholder':"Wpisz numer telefonu"}),
		}
		labels = {
			'phoneNumber': ('Numer Telefonu'),
		}


class kontakt(forms.Form):

	#imie
	#nazwisko
	#email
	#tresc
	imie=forms.CharField(label="Imię", max_length=64, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'class':"form-control",
		'id':"name", 
		'placeholder':"Podaj imię"})
	)
	nazwisko=forms.CharField(label="Nazwisko", max_length=64, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'class':"form-control",
		'id':"surname", 
		'placeholder':"Podaj nazwisko"})

	)
	email=forms.CharField(label='E-mail', max_length=40, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'class':"form-control",
		'id':"email", 
		'placeholder':"Wpisz e-mail"})
	)
	tresc=forms.CharField(label='Wiadomość', widget=forms.Textarea(
		attrs={
		'type':"text", 
		'class':"form-control",
		'id':"messageContent", 
		'placeholder':"Treść wiadomości"})
	)
