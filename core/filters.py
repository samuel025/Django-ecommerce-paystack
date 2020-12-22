import django_filters
from django_filters import CharFilter
from django.forms.widgets import TextInput
from .models import *

class ItemFilter(django_filters.FilterSet):
	title = CharFilter(field_name='title', lookup_expr='icontains', widget=TextInput(attrs={
		'placeholder': 'search',
		'class': 'form-control'
		}))
	class Meta:
		model = Item
		fields = ['title', 'category']