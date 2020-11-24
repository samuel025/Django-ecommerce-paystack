from django import forms

PAYMENT_CHOICES = (
	('S', 'Stripe'),
	('P', 'Paypal')
	)

class CheckoutForm(forms.Form):
	street_address = forms.CharField(widget=forms.TextInput(attrs={
			'placeholder':'1234 main str',
			'class': 'form-control'
		}))
	apartment_address = forms.CharField(required = False, widget=forms.TextInput(attrs={
			'placeholder':'Apartment or Suite',
			'class': 'form-control'
		}))
	phone_number = forms.CharField( widget=forms.TextInput(attrs={
			'placeholder':'Phone Number',
			'class': 'form-control'
		}))
	same_shipping_address = forms.BooleanField(required=False)
	save_info = forms.BooleanField(required=False)
	payment_option = forms.ChoiceField(widget=forms.RadioSelect,choices=PAYMENT_CHOICES)