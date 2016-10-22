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
	nazwaSzkoly=forms.CharField(label="NazwaSzkoly", max_length=100, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'class':"form-control",
		'id':"ns", 
		'placeholder':"Wpisz nazwę szkoły"})
	)
	login=forms.CharField(label='login', max_length=100, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'class':"form-control",
		'id':"username", 
		'placeholder':"Wpisz login"}) 

	)

	haslo=forms.CharField(label='haslo', max_length=100, widget=forms.PasswordInput(
		attrs={
		'type':"text", 
		'class':"form-control",
		'id':"psw", 
		'placeholder':"Wpisz haslo"})

	)
	email=forms.CharField(label='email', max_length=40, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'class':"form-control",
		'id':"email", 
		'placeholder':"Wpisz e-mail"})
	)
	numerTelefonu=forms.IntegerField(label='numerTelefonu', widget=forms.TextInput(
		attrs={
		'type':"text", 
		'class':"form-control",
		'id':"email", 
		'placeholder':"Wpisz e-mail"})
	) 
	confirm=forms.BooleanField(label='confirm')