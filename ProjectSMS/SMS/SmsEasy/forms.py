from django import forms

class addStudent(forms.Form):
	imie = forms.CharField(label='Imie', max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'class':'',
		'id':'imieUcznia',
		'size':'20',
		'placeholder':"np. Paweł"})
		
	)

	nazwisko = forms.CharField(label='Nazwisko', max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'nazwiskoUcznia',
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
		'size':'20',
		'placeholder':"Miejscowosc"})
		
	)

	ulica = forms.CharField(max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'ulica',
		'size':'20',
		'placeholder':"ulica"})
		
	)

	nrbudynku = forms.CharField(label='Nr.bud', required=False, max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'nrbud',
		'size':'4',
		'placeholder':"Nr.bud"})
		
	)
	nrmieszkania = forms.CharField(label='Nr.miesz', required=False, max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'nrmiesz',
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
		'size':'20',
		'placeholder':"Miejscowosc"})
		
	)

	ulica2 = forms.CharField(max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'ulica2',
		'size':'20',
		'placeholder':"ulica"})
		
	)

	nrbudynku2 = forms.CharField(label='Nr.bud', required=False, max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'nrbud2',
		'size':'4',
		'placeholder':"Nr.bud"})
		
	)

	nrmieszkania2 = forms.CharField(label='Nr.miesz', required=False, max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'nrmiesz2',
		'size':'5',
		'placeholder':"Nr.miesz"})
		
	)

	ocenPol = forms.CharField(label='Ocena Polski', max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'ocenPol',
		'size':'1'})
		
	)

	ocenMat = forms.CharField(label='Ocena Matematyka', max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'ocenMat',
		'size':'1'})
		
	)

	ocenAng = forms.CharField(label='Ocena Angielski', max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'ocenAng',
		'size':'1'})
		
	)

	ocenNiem = forms.CharField(label='Ocena Niemiecki', max_length=48, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'id':'ocenNiem',
		'size':'1'})
		
	)

Subjects = (
("s","Wybierz przedmiot"),	
('polski', 'polski'),
('angielski' ,'angielski'),
('niemiecki' ,'niemiecki'),
('francuski' ,'francuski'),
('wloski' ,'wloski'),
('hiszpanski' ,'hiszpanski'),
('rosyjski' ,'rosyjski'),
('matematyka' ,'matematyka'),
('fizyka' ,'fizyka'),
('informatyka' ,'informatyka'),
('historia' ,'historia'),
('biologia' ,'biologia'),
('chemia' ,'chemia'),
('geografia' ,'geografia'),
('wos' ,'wos'),
('zajęcia techniczne' ,'zajęcia techniczne'),
('zajęcia artystyczne' ,'zajęcia artystyczne'),
('edukacja dla bezpieczeństwa' ,'edukacja dla bezpieczeństwa'),
('plastyka' ,'plastyka'),
('muzyka' ,'muzyka'),
('wf' ,'wf'),
('religia/etyka' ,'religia/etyka'),
('zachowanie' ,'zachowanie'),
('Świadectwo z wyróżnieniem' ,'Świadectwo z wyróżnieniem'),
('Wynik egzaminu gimnazjalnego z języka polskiego','Wynik egzaminu gimnazjalnego z języka polskiego'),
('Wynik egzaminu gimnazjalnego z matematyki','Wynik egzaminu gimnazjalnego z matematyki'),
('Wynik egzaminu gimnazjalnego z historii i wosu','Wynik egzaminu gimnazjalnego z historii i wosu'),
('Wynik egzaminu gimnazjalnego z przedmiotów przyrodniczych' ,'Wynik egzaminu gimnazjalnego z przedmiotów przyrodniczych'),
('Wynik egzaminu gimnazjalnego z języka obcego na poziomie podstawowym' ,'Wynik egzaminu gimnazjalnego z języka obcego na poziomie podstawowym'),
('Wynik egzaminu gimnazjalnego z języka obcego na poziomie rozszerzonym' ,'Wynik egzaminu gimnazjalnego z języka obcego na poziomie rozszerzonym'),
    )

class profilAndChoice(forms.Form):
	
	
	
	profil = forms.CharField(required=True, max_length= 50,widget= forms.TextInput(
	attrs= {
	'type':"text", 
	'id':'profile',
	'size':'20',
	'placeholder':"Profil"
	}))
	
	stala_wielkosc= forms.BooleanField(required=False, label="Stała wielkość")
	
	wielkosc = forms.CharField( max_length= 2,widget= forms.TextInput(
	attrs= {
	'type':"text", 
	'id':'profile',
	'size':'5',
	'placeholder':"Wielkość"
	}))

	studentFile = forms.FileField(required=True)
	
	CopySubjects = forms.CharField(label = "",widget= forms.TextInput(
	attrs= {
	'type':"hidden", 
	'name':'CopySubjects',
	'id':"AllSubjects"
	}))
	przedmioty = forms.ChoiceField(
		
        label="Przedmioty",
        choices=Subjects,
        widget=forms.Select(attrs= {
	'name':'subject',
	'id':'subject'
	
	})

	)
	error_messages = {
        'profil': {
            'invalid': ("Podaj nazwe prfilu"),
            },
        'File':{
        	'invalid': ('Podaj nazwe prfilu'),
        }, 
    }
