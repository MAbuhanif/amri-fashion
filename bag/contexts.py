from decimal import Decimal
from django.conf import settings
from products.models import Product


def bag_contents(request):
    """Calculate the bag contents and totals."""
    bag = request.session.get('bag', {})
    bag_items = []
    total = 0
    product_count = 0

    for item_id, item_data in bag.items():
        if isinstance(item_data, dict):
            for size, quantity in item_data['items_by_size'].items():
                product = Product.objects.get(pk=item_id)
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                    'product': product,
                    'quantity': quantity,
                    'size': size,
                    'subtotal': quantity * product.price,
                })
        else:
            product = Product.objects.get(pk=item_id)
            total += item_data * product.price
            product_count += item_data
            bag_items.append({
                'product': product,
                'quantity': item_data,
                'subtotal': item_data * product.price,
            })

    delivery = Decimal(settings.STANDARD_DELIVERY_PERCENTAGE)
    free_delivery_delta = max(Decimal(settings.FREE_DELIVERY_THRESHOLD) - total, 0)
    grand_total = total + delivery if free_delivery_delta > 0 else total

    return {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery if free_delivery_delta > 0 else 0,
        'free_delivery_delta': free_delivery_delta,
        'grand_total': grand_total,
    }
