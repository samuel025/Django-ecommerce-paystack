from django.contrib import admin
from .models import Item, OrderItem, Order, Address, Payment
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
	list_display = ['user', 
					'ordered',
					'being_delivered',
					'recieved',
					'shipping_address', 
					'payment', 
					
					]
	list_display_links = ['user', 'shipping_address', 'payment']
	list_filter = ['ordered',
					'being_delivered',
					'recieved'
					]
	search_fields = ['user__username',
					 'ref_code'
				]
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'phone_number',
        'default'
    ]
    list_filter = ['default']
    search_fields = ['user__username', 'street_address', 'apartment_address']



admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Payment)



