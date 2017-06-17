from django import forms


class addProfile(forms.Form):
	newProfileFullName = forms.CharField(label='Pełna nazwa profilu', max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'class':"form-control",
		'id':'ProfileFullName',
		'size':'20',
		'placeholder':"np. Technik Informatyk"})
		
	)
	newProfileShortName = forms.CharField(label='Skrótowa nazwa profilu', max_length=8,
		widget=forms.TextInput(
			attrs={
			'type':"text", 
			'class':"form-control",
			'id':'ProfileShortName',
			'size':'20',
			'placeholder':"np. TI"})
		
	)
	
class addStudent(forms.Form):
	imie = forms.CharField(label='Imie', max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text",
		'class':"form-control",
		'id':'imieUcznia',
		'size':'20',
		'placeholder':"np. Paweł"})
		
	)

	nazwisko = forms.CharField(label='Nazwisko', max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'nazwiskoUcznia',
		'class':"form-control",
		'size':'20',
		'placeholder':"np. Sagan"})
		
	)

	# ADRES ZAMIESZKANIA
	kod1 = forms.CharField(widget=forms.TextInput(attrs={'id':'kod_p1','class':'kodp','maxlength':'2','size':'1'}))
	kod2 = forms.CharField(widget=forms.TextInput(attrs={'id':'kod_p2','class':'kodp','maxlength':'3','size':'2'}))

	miejscowosc = forms.CharField(max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'miejscowosc',
		'class':"form-control",
		'size':'20',
		'placeholder':"Miejscowosc"})
		
	)

	ulica = forms.CharField(max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'ulica',
		'class':"form-control",
		'size':'14',
		'placeholder':"ulica"})
		
	)

	nrbudynku = forms.CharField(label='Nr.bud', required=False, max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'nrbud',
		'class':"form-control",
		'size':'4',
		'placeholder':"Nr.bud"})
		
	)
	nrmieszkania = forms.CharField(label='Nr.miesz', required=False, max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'nrmiesz',
		'class':"form-control",
		'size':'5',
		'placeholder':"Nr.miesz"})
		
	)

	# ADRES ZAMELDOWANIA
	kod12 = forms.CharField(widget=forms.TextInput(attrs={'id':'kod_p21','class':'kodp','maxlength':'2','size':'1'}))
	kod22 = forms.CharField(widget=forms.TextInput(attrs={'id':'kod_p22','class':'kodp','maxlength':'3','size':'1'}))

	miejscowosc2 = forms.CharField(max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'miejscowosc2',
		'class':"form-control",
		'size':'20',
		'placeholder':"Miejscowosc"})
		
	)

	ulica2 = forms.CharField(max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'ulica2',
		'class':"form-control",
		'size':'14',
		'placeholder':"ulica"})
		
	)

	nrbudynku2 = forms.CharField(label='Nr.bud', required=False, max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'nrbud2',
		'class':"form-control",
		'size':'4',
		'placeholder':"Nr.bud"})
		
	)

	nrmieszkania2 = forms.CharField(label='Nr.miesz', required=False, max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'nrmiesz2',
		'class':"form-control",
		'size':'5',
		'placeholder':"Nr.miesz"})
		
	)

	ocenPol = forms.CharField(label='Ocena Polski', max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'ocenPol',
		'class':"form-control",
		'size':'1'})
		
	)

	ocenMat = forms.CharField(label='Ocena Matematyka', max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'ocenMat',
		'class':"form-control",
		'size':'1'})
		
	)

	ocenAng = forms.CharField(label='Ocena Angielski', max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'ocenAng',
		'class':"form-control",
		'size':'1'})
		
	)

	ocenNiem = forms.CharField(label='Ocena Niemiecki', max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'ocenNiem',
		'class':"form-control",
		'size':'1'})
		
	)

class formEditStudent(forms.Form):
	imie = forms.CharField(label='Imie', max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'class':"form-control",
		'id':'imieUcznia',
		'size':'20',
		'placeholder':"np. Paweł"})
		
	)

	nazwisko = forms.CharField(label='Nazwisko', max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'nazwiskoUcznia',
		'class':"form-control",
		'size':'20',
		'placeholder':"np. Sagan"})
		
	)

	# ADRES ZAMIESZKANIA
	kod1 = forms.CharField(widget=forms.TextInput(attrs={'id':'kod_p1','class':'kodp','maxlength':'2','size':'1'}))
	kod2 = forms.CharField(widget=forms.TextInput(attrs={'id':'kod_p2','class':'kodp','maxlength':'3','size':'2'}))

	miejscowosc = forms.CharField(max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'miejscowosc',
		'class':"form-control",
		'size':'20',
		'placeholder':"Miejscowosc"})
		
	)

	ulica = forms.CharField(max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'ulica',
		'class':"form-control",
		'size':'20',
		'placeholder':"ulica"})
		
	)

	nrbudynku = forms.CharField(label='Nr.bud', required=False, max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'nrbud',
		'class':"form-control",
		'size':'4',
		'placeholder':"Nr.bud"})
		
	)
	nrmieszkania = forms.CharField(label='Nr.miesz', required=False, max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'nrmiesz',
		'class':"form-control",
		'size':'5',
		'placeholder':"Nr.miesz"})
		
	)

	# ADRES ZAMELDOWANIA
	kod12 = forms.CharField(widget=forms.TextInput(attrs={'id':'kod_p21','class':'kodp','maxlength':'2','size':'1'}))
	kod22 = forms.CharField(widget=forms.TextInput(attrs={'id':'kod_p22','class':'kodp','maxlength':'3','size':'1'}))

	miejscowosc2 = forms.CharField(max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'miejscowosc2',
		'class':"form-control",
		'size':'20',
		'placeholder':"Miejscowosc"})
		
	)

	ulica2 = forms.CharField(max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'ulica2',
		'size':'20',
		'class':"form-control",
		'placeholder':"ulica"})
		
	)

	nrbudynku2 = forms.CharField(label='Nr.bud', required=False, max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'nrbud2',
		'size':'4',
		'class':"form-control",
		'placeholder':"Nr.bud"})
		
	)

	nrmieszkania2 = forms.CharField(label='Nr.miesz', required=False, max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'nrmiesz2',
		'size':'5',
		'class':"form-control",
		'placeholder':"Nr.miesz"})
		
	)

	klasa = forms.ChoiceField(label='klasa')

	ocenPol = forms.CharField(label='Ocena Polski', max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'ocenPol',
		'class':"form-control",
		'size':'1'})
		
	)

	ocenMat = forms.CharField(label='Ocena Matematyka', max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'ocenMat',
		'class':"form-control",
		'size':'1'})
		
	)

	ocenAng = forms.CharField(label='Ocena Angielski', max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'ocenAng',
		'class':"form-control",
		'size':'1'})
		
	)

	ocenNiem = forms.CharField(label='Ocena Niemiecki', max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'ocenNiem',
		'class':"form-control",
		'size':'1'})
		
	)

	iducznia = forms.CharField(max_length=32, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'iducznia',
		'class':"form-control",
		'hidden':'True'})
		
	)

	def __init__(self,*args, **kwargs):
		klasyVar = kwargs.pop('klasy', None)
		super(formEditStudent, self).__init__(*args, **kwargs)
		self.fields['klasa'].choices = klasyVar

class removeClass(forms.Form):
	klasy = forms.ChoiceField(label='Usun')

	def __init__(self,*args, **kwargs):
		klasyVar = kwargs.pop('klasy', None)
		super(removeClass, self).__init__(*args, **kwargs)
		self.fields['klasy'].choices = klasyVar


class removeProfile(forms.Form):
	profile = forms.ChoiceField(label='Usun')

	def __init__(self,*args, **kwargs):
		profilesVar = kwargs.pop('profile', None)
		super(removeProfile, self).__init__(*args, **kwargs)
		self.fields['profile'].choices = profilesVar

class removeAlgorithm(forms.Form):
	algorithm = forms.ChoiceField(label='Usun')

	def __init__(self,*args, **kwargs):
		algorithmVar = kwargs.pop('algorytm', None)
		super(removeAlgorithm, self).__init__(*args, **kwargs)
		self.fields['algorithm'].choices = algorithmVar

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

class addAlgorithm(forms.Form):
	nazwa = forms.CharField(label='Nazwa algorytmu',widget=forms.TextInput(
		attrs={
		'type':"text",
		'class':"form-control",
		'size':'20'})	
	)

	matematyka = forms.IntegerField(label='Matematyka',widget=forms.TextInput(
		attrs={
		'type':"text",
		'class':"form-control",
		'size':'20'})
	)

	jpolski = forms.IntegerField(label='Język polski',widget=forms.TextInput(
		attrs={
		'type':"text",
		'class':"form-control",
		'size':'20'})
	)

	jangielski = forms.IntegerField(label='Język Angielski',widget=forms.TextInput(
		attrs={
		'type':"text",
		'class':"form-control",
		'size':'20'})
	)

	jniemiecki = forms.IntegerField(label='Język Niemiecki',widget=forms.TextInput(
		attrs={
		'type':"text",
		'class':"form-control",
		'size':'20'})
	)

class fillClass(forms.Form):
	klasy = forms.ChoiceField(label='Wybierz klase')
	sposob = forms.BooleanField(label='Optymalizuj',required=False)

	def __init__(self,*args, **kwargs):
		klasyVar = kwargs.pop('klasy', None)
		super(fillClass, self).__init__(*args, **kwargs)
		self.fields['klasy'].choices = klasyVar

class removeCopy(forms.Form):
	nazwaKopii = forms.ChoiceField(label = '',widget=forms.Select(attrs={'class':'selectUsunKopie'}))

	def __init__(self,*args, **kwargs):
		kopieVar = kwargs.pop('kopie', None)
		super(removeCopy, self).__init__(*args, **kwargs)
		self.fields['nazwaKopii'].choices = kopieVar

class makeCopy(forms.Form):
	nazwaKopii = forms.CharField(label='',max_length=48, widget=forms.TextInput(
		attrs={
		'type':'text',
		'class':"form-control",
		'size':'13',
		'placeholder':'Nazwa kopii'
		})
	)

class restoreCopy(forms.Form):
	nazwaKopii = forms.ChoiceField(label = '',widget=forms.Select(attrs={'class':'selectUsunKopie'}))

	def __init__(self,*args, **kwargs):
		kopieVar = kwargs.pop('kopie', None)
		super(restoreCopy, self).__init__(*args, **kwargs)
		self.fields['nazwaKopii'].choices = kopieVar