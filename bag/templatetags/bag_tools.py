from django import template

register = template.Library()


@register.filter
def calc_subtotal(price, quantity):
    """Calculate the subtotal for a line item."""
    return price * quantity
