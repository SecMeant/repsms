from django import forms


class addProfile(forms.Form):
	newProfileFullName=forms.CharField(label='Pełna nazwa profilu', max_length=16, widget=forms.TextInput(
		attrs={
		'type':"text", 
		'class':"form-control",
		'id':'ProfileFullName',
		'placeholder':"np. Technik Informatyk"})
		
	)
	newProfileShortName=forms.CharField(label='Skrótowa nazwa profilu', max_length=8,
		widget=forms.TextInput(
			attrs={
			'type':"text", 
			'class':"form-control",
			'id':'ProfileShortName',
			'placeholder':"np. TI"})
		
	)