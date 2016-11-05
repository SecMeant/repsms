from django import forms


class addProfile(forms.Form):
	newProfileFullName = forms.CharField(label='Pełna nazwa profilu', max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'class':"form-control",
		'id':'ProfileFullName',
		'placeholder':"np. Technik Informatyk"})
		
	)
	newProfileShortName = forms.CharField(label='Skrótowa nazwa profilu', max_length=8,
		widget=forms.TextInput(
			attrs={
			'type':"text", 
			'class':"form-control",
			'id':'ProfileShortName',
			'placeholder':"np. TI"})
		
	)
	
class addStudent(forms.Form):
	imie = forms.CharField(label='Imie', max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'class':"form-control",
		'id':'imieUcznia',
		'placeholder':"np. Paweł"})
		
	)

	nazwisko = forms.CharField(label='Nazwisko', max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'class':"form-control",
		'id':'nazwiskoUcznia',
		'placeholder':"np. Sagan"})
		
	)

	pesel = forms.CharField(label='Pesel', max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'class':"form-control",
		'id':'peselUcznia',
		'placeholder':"np. 97070904998"})
		
	)

class addClass(forms.Form):
	nazwaKlasy = forms.CharField(label='Nazwa klasy', max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'class':"form-control",
		'id':'nazwaKlasy',
		'placeholder':"nazwa"})
		
	)
	liczebnosc = forms.IntegerField(label='Liczebnosc klasy')
	profil = forms.ChoiceField(label='Profil')
	algorytm = forms.ChoiceField(label='Algorytm')



	def __init__(self,*args, **kwargs):
		profile = kwargs.pop('profile', None)
		algorytmVar = kwargs.pop('algorytm', None)
		super(addClass, self).__init__(*args, **kwargs)
		self.fields['profil'].choices = profile
		self.fields['algorytm'].choices = algorytmVar
		print(algorytmVar)
		print(profile)

class addAlgorithm(forms.Form):
	nazwa = forms.CharField(label='Nazwa algorytmu')
	matematyka = forms.IntegerField(label='Matematyka')
	jpolski = forms.IntegerField(label='Język polski')
	jangielski = forms.IntegerField(label='Język Angielski')
	jniemiecki = forms.IntegerField(label='Język Niemiecki')
