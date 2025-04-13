from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm


def checkout(request):
    """
    Render the checkout page.
    """
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Your shopping bag is empty.")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51ONYiKBuPuoPUdzs1H2ebSu7DVQMlnu3INiuYzLxHU18mfTmPwsRnBZDeO7MszVGzSPziyqrt0ru65rwT3P7FejY00XyERLqpc',
        'client_secret': 'test client secret',
    }
    return render(request, template, context)
