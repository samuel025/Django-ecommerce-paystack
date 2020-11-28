from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core.views import ItemDetailView, CheckoutView, HomeView, add_to_cart, remove_from_cart, OrderSummaryView, remove_single_item_from_cart, PaymentView, final_checkout, add_coupon
from dispatch import receiver
    
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home_page'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove-from-cart'),
    path('products/<slug>/', ItemDetailView.as_view(), name='product_page'),
    path('order-summary', OrderSummaryView.as_view(), name='order_summary'),
    path('remove-single-item-from-cart/<slug>', remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path('accounts/', include('allauth.urls')),
    path('verify/<int:id>', PaymentView.as_view(), name='verify_payment'),
    path('final-checkout/', final_checkout, name='f_checkout'),
    path('add-coupon/', add_coupon, name='add-coupon')
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
