import random
import string
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order, BillingAddress, Payment, Coupon
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm, CouponForm
from pypaystack import Transaction
from django.http import JsonResponse
# Create your views here.

def create_ref_code():
	return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

def products(request):
	context = {
		
	}
	return render(request, "product-page.html", context)


class CheckoutView(View):
	def get(self, *args, **kwargs):	
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			form = CheckoutForm()
			context={
			'form': form,
			'order': order,
			'couponform' : CouponForm(),
			'DISPLAY_COUPON': True
			}

		except ObjectDoesNotExist:
			messages.info(self.request, "You do not have an active order")
			return redirect("checkout")
		
		return render(self.request, "checkout-page.html", context)

	def post(self, *args, **kwargs):
		form = CheckoutForm(self.request.POST or None)
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			if form.is_valid():
				street_address = form.cleaned_data.get('street_address')
				apartment_address = form.cleaned_data.get('apartment_address')
				phone_number = form.cleaned_data.get('phone_number')
				# same_shipping_address = form.cleaned_data.get('same_shipping_address')
				# save_info = form.cleaned_data.get('save_info')
				payment_option = form.cleaned_data.get('payment_option')
				billing_address = BillingAddress(
						user = self.request.user,
						street_address = street_address,
						apartment_address = apartment_address,
						phone_number = phone_number,
					) 
				billing_address.save()
				order.billing_address = billing_address
				order.save()
				return redirect('f_checkout')
			return redirect('checkout')
		except ObjectDoesNotExist:
			messages.error(self.request, "You do not have active orders")
			return redirect('checkout')

class HomeView(ListView):
	model = Item
	template_name = "home-page.html"

class ItemDetailView(DetailView):
	model = Item
	template_name = "product-page.html"

@login_required
def add_to_cart(request, slug):
	item = get_object_or_404(Item, slug=slug)
	order_item, created = OrderItem.objects.get_or_create(
		item=item,
		user=request.user,
		ordered=False
		)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		if order.items.filter(item__slug=item.slug).exists():
			order_item.quantity += 1
			order_item.save()
			messages.info(request, "This item was quantity was updated")
			return redirect('order_summary')
		else:
			messages.info(request, "This item was added to your cart")
			order.items.add(order_item)
			return redirect('order_summary')
	else:
		ordered_date = timezone.now()
		order = Order.objects.create(user=request.user, ordered_date=ordered_date)
		order.items.add(order_item)
		messages.info(request, "This item was added to your cart")
		return redirect('order_summary')
	
@login_required
def remove_from_cart(request,slug):
	item = get_object_or_404(Item, slug=slug)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		if order.items.filter(item__slug=item.slug).exists():
			order_item = OrderItem.objects.filter(
					item=item,
					user=request.user,
					ordered=False
			)[0]
			order.items.remove(order_item)
			messages.info(request, "This item was removed from your cart")
			return redirect('order_summary')
		else:
			messages.info(request, "This item is not in your cart")
			return redirect('product_page', slug=slug)	
	else:
		messages.info(request, "You do not have an active order")
		return redirect('product_page', slug=slug)
	
class OrderSummaryView(LoginRequiredMixin, View):
	def get(self, *args, **kwargs):
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			context ={
				'object': order
			}
			return render(self.request, 'order_summary.html', context)
		except ObjectDoesNotExist:
			messages.error(self.request, "You do not have an active order")
			return redirect("/")
		

@login_required
def remove_single_item_from_cart(request,slug):
	item = get_object_or_404(Item, slug=slug)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		if order.items.filter(item__slug=item.slug).exists():
			order_item = OrderItem.objects.filter(
					item=item,
					user=request.user,
					ordered=False
			)[0]
			if order_item.quantity > 1:
				order_item.quantity -= 1
				order_item.save()
			else:
				order.items.remove(order_item)
			messages.info(request, "This item quantity was updated")
			return redirect('order_summary')
		else:
			messages.info(request, "This item is not in your cart")
			return redirect('product_page', slug=slug)	
	else:
		messages.info(request, "You do not have an active order")
		return redirect('product_page', slug=slug)



def final_checkout(request):
	order = Order.objects.get(user=request.user, ordered=False)
	if order.billing_address:
		context = {
					'order':order,
					'DISPLAY_COUPON': False

					}
		return render(request, 'final_checkout.html', context)
	else:
		messages.warning(request, "You have not submitted any address")
		return redirect('checkout')



class PaymentView(View):
	def get(self, *args, **kwargs):
		transaction = Transaction(authorization_key = 'sk_test_4efc8832170a975a1e1eb669a89b512909d0049a')
		response = transaction.verify(kwargs['id'])
		data = JsonResponse(response, safe=False)

		if response[3]:
			try:
				order = Order.objects.get(user=self.request.user, ordered=False)
				payment = Payment()
				payment.paystack_id = kwargs['id']
				payment.user = self.request.user
				payment.amount = order.get_total()
				payment.save()

				order_items = order.items.all()
				order_items.update(ordered=True)
				for item in order_items:
					item.save()

				order.ordered = True
				order.payment = payment
				order.ref_code = create_ref_code()
				order.save()

				messages.success(self.request, "order was successful")
				return redirect("/")
			except ObjectDoesNotExist:
				messages.success(self.request, "Your order was successful")
				return redirect("/")
		else:
			messages.danger(self.request, "Could not verify the transaction")
			return redirect("/")

def get_coupon(request, code):
	try:
		coupon = Coupon.objects.get(code=code)
		return coupon
	except ObjectDoesNotExist:
		messages.info(request, "This coupon does not exist")
		return redirect("checkout")


class add_coupon(View):
	def post(self, *args, **kwargs):
		if self.request.method == "POST":
			form = CouponForm(self.request.POST or None)
			if form.is_valid():
				try:
					code = form.cleaned_data.get('code')
					order = Order.objects.get(user=self.request.user, ordered=False)
					order.coupon = get_coupon(self.request, code)
					order.save()
					messages.success(self.request, "successfuly added coupon")
					return redirect("checkout")

				except ObjectDoesNotExist:
					messages.info(self.request, "You do not have an active order")
					return redirect("checkout")
		

	
