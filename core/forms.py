from django import forms


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
	

class CouponForm(forms.Form):
	code = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control',
		'placeholder': 'Promo Code',
		'aria-label': 'Recipient\'s username',
		'aria-describedby': 'basic-addon2'
		}))