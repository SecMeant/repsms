from django import forms
from .models import User
from django.forms import ModelForm
import sqlite3,os
from django.contrib.auth import authenticate

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class logowanie(forms.Form):

	login=forms.CharField(label='Login', max_length=100,
		widget=forms.TextInput(
			attrs={
			'type':"text", 
			'class':"form-control",
			'id':"username", 
			'placeholder':"Wpisz login"})
		
	)
	haslo=forms.CharField(label='Haslo', max_length=100, widget=forms.PasswordInput(
		attrs={
		'type':"password", 
		'class':"form-control",
		'id':"psw", 
		'placeholder':"Wpisz haslo"})
		
	)
	def __init__(self, *args, **kwargs):
		super(logowanie, self).__init__(*args, **kwargs)
		if self.errors:
			for f_name in self.fields:
				if f_name in self.errors:
					classes = self.fields[f_name].widget.attrs.get('class', '')
					ids = self.fields[f_name].widget.attrs.get('id', '')
					classes += ' form-control'
					ids += ' inputError'
					self.fields[f_name].widget.attrs['class'] = classes
					self.fields[f_name].widget.attrs['id'] = ids
	def clean(self):
		'''Required custom validation for the form.'''
		super(logowanie , self).clean()
		if 'haslo' in self.cleaned_data and 'login' in self.cleaned_data:
			self.userr = authenticate(username=self.cleaned_data['login'], password=self.cleaned_data['haslo'])
			if self.userr == None:
				self._errors['login'] = [u' ']
				self._errors['haslo'] = [u'Wprowadź poprawne dane logowania ']



class rejestracja(ModelForm):
	def __init__(self, *args, **kwargs):
		super(rejestracja, self).__init__(*args, **kwargs)
		if self.errors:
			for f_name in self.fields:
				if f_name in self.errors:
					classes = self.fields[f_name].widget.attrs.get('class', '')
					ids = self.fields[f_name].widget.attrs.get('id', '')
					classes += ' form-control'
					ids += ' inputError'
					self.fields[f_name].widget.attrs['class'] = classes
					self.fields[f_name].widget.attrs['id'] = ids


	def clean(self):
		'''Required custom validation for the form.'''
		super(rejestracja,self).clean()
		if 'password' in self.cleaned_data and 'passwordConfirm' in self.cleaned_data:
			if self.cleaned_data['password'] != self.cleaned_data['passwordConfirm'] or self.cleaned_data['password'] == 0 :
				self._errors['password'] = [u'Hasła się nie zgadzają.']
				self._errors['passwordConfirm'] = [u'Hasła się nie zgadzają.']
		
		if 'phoneNumber' in self.cleaned_data:
			temp=self.cleaned_data['phoneNumber']
			temp=str(temp).replace("+", "")
			temp=str(temp).replace(" ", "")
			temp=str(temp).replace("(", "")
			temp=str(temp).replace(")", "")
			temp=str(temp).replace("-", "")
			if not len(str(temp)) >=9 or not str(temp).isdigit():
				self._errors['phoneNumber'] = [u'Podaj prawidlowy numer telefonu.']
		if 'username' in self.cleaned_data:
			try:
				User.objects.get(username=self.cleaned_data['username'])
				self._errors['username'] = [u'Nazwa jest już zajęta.']
			except:
				pass
		return self.cleaned_data


	passwordConfirm=forms.CharField(label="Potwierdzenie hasła", max_length=64, widget=forms.PasswordInput(
	attrs={
	'type':"password", 
	'class':"form-control",
	'id':"passwordConfirm", 
	'placeholder':"Potwierdź hasło"})
	)

	class Meta:
		model = User
		fields = ('nazwaSzkoly', 'username', 'email', 'password', 'passwordConfirm', 'phoneNumber')
		widgets = {
		'username': forms.TextInput(
			attrs={
			'type':"text", 
			'class':"form-control",
			'id':"username", 
			'placeholder':"Wpisz login"}),

		'nazwaSzkoly': forms.TextInput(
			attrs={
			'type':"text", 
			'class':"form-control",
			'id':"nazwaSzkoly", 
			'placeholder':"Wpisz nazwe szkoly",
			'required':'required'}),

		'password': forms.PasswordInput(
			attrs={
			'type':"password", 
			'class':"form-control",
			'id':"password", 
			'placeholder':"Wpisz hasło"}),
		
		'phoneNumber': forms.TextInput(
			attrs={
			'type':"text", 
 			'class':"form-control",
			'id':"phoneNumber", 
			'placeholder':"Wpisz numer telefonu"}),		

		'email': forms.TextInput(
			attrs={
			'type':"email", 
			'class':"form-control",
			'id':"email", 
			'placeholder':"Wpisz email"}),
		}
		labels = {
			'nazwaSzkoly': ('Nazwa Szkoły'),
			'username': ('Login'),
			'password': ('Hasło'),
			'phoneNumber': ('Numer Telefonu'),
			'email': ('E-mail'),
		}
		error_messages = {
            'email': {
                'invalid': ("Podaj poprawny adres email."),
                'unique':("Konto o takim adresie email istniej.")
            },
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
	email=forms.EmailField(label='E-mail', max_length=40, widget=forms.TextInput(
		attrs={
		'type':"email", 
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

	error_messages = {
            'email': {
                'invalid': ("Podaj poprawny adres email."),
            },
            'imei': {
                'invalid': ("Podaj imię."),
            },
            'nazwisko': {
                'invalid': ("Podaj nazwisko."),
            },
            'tresc': {
                'invalid': ("O co chciałbyś nas spytać ?"),
            },
        }
	def __init__(self, *args, **kwargs):
		super(kontakt, self).__init__(*args, **kwargs)
		if self.errors:
			for f_name in self.fields:
				if f_name in self.errors:
					classes = self.fields[f_name].widget.attrs.get('class', '')
					ids = self.fields[f_name].widget.attrs.get('id', '')
					classes += ' form-control'
					ids += ' inputError'
					self.fields[f_name].widget.attrs['class'] = classes
					self.fields[f_name].widget.attrs['id'] = ids
	# def clean(self):
	# 	'''Required custom validation for the form.'''
	# 	super(kontakt , self).clean()
	# 	if 'imie' in self.cleaned_data and 'nazwisko' in self.cleaned_data and  'email' in self.cleaned_data and 'tresc' in self.cleaned_data :
	# 		if self.cleaned_data['imie'] == "":
	# 			_errors['imie'] = "Pole nie może być puste"
			


class ChangePassword(forms.Form):

	password=forms.CharField(label='Hasło', max_length=100,
		widget=forms.PasswordInput(
			attrs={
			'type':"password", 
			'class':"form-control",
			'id':"psw", 
			'placeholder':"Hasło:"})
		
	)
	passwordConfirm=forms.CharField(label='Powtórz hasło:', max_length=100, widget=forms.PasswordInput(
		attrs={
		'type':"password", 
		'class':"form-control",
		'id':"psw", 
		'placeholder':"Hasło:"})
		
	)
	superKey=forms.CharField(label='Klucz:', max_length=100, widget=forms.PasswordInput(
		attrs={
		'type':"password", 
		'class':"form-control",
		'id':"psw", 
		'placeholder':"Klucz:"})
		
	)

	def __init__(self, *args, **kwargs):
		super(ChangePassword, self).__init__(*args, **kwargs)
		if self.errors:
			for f_name in self.fields:
				if f_name in self.errors:
					classes = self.fields[f_name].widget.attrs.get('class', '')
					ids = self.fields[f_name].widget.attrs.get('id', '')
					classes += ' form-control'
					ids += ' inputError'
					self.fields[f_name].widget.attrs['class'] = classes
					self.fields[f_name].widget.attrs['id'] = ids
	def clean(self):
		'''Required custom validation for the form.'''
		super(ChangePassword , self).clean()
		if 'password' in self.cleaned_data and 'passwordConfirm' in self.cleaned_data:
			if self.cleaned_data['password'] != self.cleaned_data['passwordConfirm']:
				self._errors['password'] = [u""]
				self._errors['passwordConfirm'] = [u"Hasła nie mogą się różnić"]
		if 'superKey' in self.cleaned_data:
			try:
				conn=sqlite3.connect(os.path.join(BASE_DIR,"UserTempChangePassword.db"))
				c = conn.cursor()
				c.execute('SELECT * FROM User WHERE key=(?) ' ,[self.cleaned_data['superKey']])
				
				if len(c.fetchall()) is not  1:
					conn.close()
					raise ValueError
				conn.close()
			except ValueError:
				self._errors['superKey'] = [u"Niepoprawny kod"]