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