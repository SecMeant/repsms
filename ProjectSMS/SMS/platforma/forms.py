from django import forms

class logowanie(forms.Form):
	haslo=forms.CharField(label='haslo', max_length=100, widget=forms.PasswordInput(
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
class rejestracja(forms.Form):
	# nazwa szkoły
	# login
	# haslo
	# email
	# numer telefonu
	# checkbox accept regulaminu
	nazwaSzkoly=forms.CharField(label="Nazwa Szkoły", max_length=100, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'class':"form-control",
		'id':"ns", 
		'placeholder':"Wpisz nazwę szkoły"})
	)
	login=forms.CharField(label='Login', max_length=100, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'class':"form-control",
		'id':"username", 
		'placeholder':"Wpisz login"}) 

	)

	haslo=forms.CharField(label='Hasło', max_length=100, widget=forms.PasswordInput(
		attrs={
		'type':"text", 
		'class':"form-control",
		'id':"psw", 
		'placeholder':"Wpisz haslo"})

	)
	email=forms.CharField(label='E-mail', max_length=40, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'class':"form-control",
		'id':"email", 
		'placeholder':"Wpisz e-mail"})
	)
	numerTelefonu=forms.IntegerField(label='NumerTelefonu', widget=forms.TextInput(
		attrs={
		'type':"text", 
		'class':"form-control",
		'id':"email", 
		'placeholder':"Wpisz e-mail"})
	) 
	confirm=forms.BooleanField(label='Confirm')

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
