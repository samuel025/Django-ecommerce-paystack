from django import forms


class CheckoutForm(forms.Form):
	street_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
			'placeholder':'1234 main str',
			'class': 'form-control'
		}))
	apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
			'placeholder':'Apartment or Suite',
			'class': 'form-control'
		}))
	phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={
			'placeholder':'Phone Number',
			'class': 'form-control'
		}))
	set_default_shipping = forms.BooleanField(required=False)
	use_default_shipping = forms.BooleanField(required=False)
	
	

