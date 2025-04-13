import stripe
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from bag.contexts import bag_contents


def checkout(request):
    """
    A view to handle the checkout process.
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Check if the bag is empty
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment.")
        return redirect(reverse('products'))

    # Calculate the total and create a Stripe PaymentIntent
    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)  # Convert to cents
    stripe.api_key = stripe_secret_key

    try:
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
    except stripe.error.StripeError as e:
        messages.error(request, "There was an issue connecting to Stripe. Please try again later.")
        return redirect(reverse('view_bag'))

    # Initialize the order form
    order_form = OrderForm()

    # Warn if the Stripe public key is missing
    if not stripe_public_key:
        messages.warning(
            request,
            "Stripe public key is missing. Did you forget to set it in your environment?"
        )

    # Render the checkout page
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)