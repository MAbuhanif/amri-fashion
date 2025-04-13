from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages


# Create your views here.

def view_bag(request):
    """ A view that renders the bag contents page """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """
    try:
        quantity = int(request.POST.get('quantity', 1))
        redirect_url = request.POST.get('redirect_url', '/')
        size = request.POST.get('product_size', None)
        bag = request.session.get('bag', {})

        if size:
            if item_id in bag:
                if size in bag[item_id]['items_by_size']:
                    bag[item_id]['items_by_size'][size] += quantity
                else:
                    bag[item_id]['items_by_size'][size] = quantity
            else:
                bag[item_id] = {'items_by_size': {size: quantity}}
        else:
            if item_id in bag:
                bag[item_id] += quantity
            else:
                bag[item_id] = quantity

        request.session['bag'] = bag
        messages.success(request, "Item successfully added to your bag!")
        return redirect(redirect_url)

    except ValueError:
        messages.error(request, "Invalid quantity provided.")
        return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adjust the quantity of the specified product to the specified amount """
    try:
        quantity = int(request.POST.get('quantity', 0))
        size = request.POST.get('product_size', None)
        bag = request.session.get('bag', {})

        if size:
            if quantity > 0:
                bag[item_id]['items_by_size'][size] = quantity
            else:
                del bag[item_id]['items_by_size'][size]
                if not bag[item_id]['items_by_size']:
                    bag.pop(item_id)
        else:
            if quantity > 0:
                bag[item_id] = quantity
            else:
                bag.pop(item_id)

        request.session['bag'] = bag
        messages.success(request, "Bag updated successfully!")
        return redirect(reverse('view_bag'))

    except ValueError:
        messages.error(request, "Invalid quantity provided.")
        return redirect(reverse('view_bag'))
    except KeyError:
        messages.error(request, "Item not found in your bag.")
        return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """ Remove the item from the shopping bag """
    try:
        size = request.POST.get('product_size', None)
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
        else:
            bag.pop(item_id)

        request.session['bag'] = bag
        messages.success(request, "Item removed from your bag.")
        return redirect('view_bag')

    except KeyError:
        messages.error(request, "Item not found in your bag.")
        return redirect('view_bag')


def example_view(request):
    messages.success(request, "This is a success message!")
    messages.error(request, "This is an error message!")
    messages.warning(request, "This is a warning message!")
    messages.info(request, "This is an info message!")
    return redirect('home')
