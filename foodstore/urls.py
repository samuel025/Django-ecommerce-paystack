from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core.views import ItemDetailView, CheckoutView, HomeView, add_to_cart, remove_from_cart, OrderSummaryView, remove_single_item_from_cart
from dispatch import receiver
from paystack.api import signals

@receiver(signals.successful_payment_signal)
def on_successful_payment(sender, **kwargs):
    import pdb

    pdb.set_trace()
    pass
    
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
    path("paystack/", include(("paystack.frameworks.django.urls", "paystack"), namespace="paystack"))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
