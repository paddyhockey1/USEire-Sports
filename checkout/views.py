from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm
from .models import Order, OrderLineItem

import stripe

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51QCGuODyLxdlHT8TwyywDVVBc6qtaFM7k4UNOFcXKxX2QwARnfswIVNOtPe1FQwTMWJcYOaGpyBpKJtUNxP8g3zq00aToXunsW',
        'client_secret': 'test_client_secret'
    }

    return render(request, template, context)