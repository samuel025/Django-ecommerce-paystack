from django.contrib import admin
from .models import Item, OrderItem, Order, BillingAddress, Payment, Coupon
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
	list_display = ['user', 
					'ordered',
					'being_delivered',
					'recieved',
					'billing_address', 
					'payment', 
					'coupon'
					]
	list_display_links = ['user', 'billing_address', 'payment', 'coupon']
	list_filter = ['ordered',
					'being_delivered',
					'recieved'
					]
	search_fields = ['user__username',
					 'ref_code'
				]



admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(BillingAddress)
admin.site.register(Payment)
admin.site.register(Coupon)