from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from products.models import Product


# Create your views here.

def view_bag(request):
    """ A view that renders the bag contents page """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """
    try:
        quantity = int(request.POST.get('quantity', 1))  # Default to 1 if quantity is not provided
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
        return redirect(redirect_url)

    except ValueError:
        return HttpResponse("Invalid quantity", status=400)


def adjust_bag(request, item_id):
    """ Adjust the quantity of the specified product to the specified amount """
    try:
        quantity = int(request.POST.get('quantity', 0))  # Default to 0 if quantity is not provided
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
        return redirect(reverse('view_bag'))

    except ValueError:
        return HttpResponse("Invalid quantity", status=400)
    except KeyError:
        return HttpResponse("Item not found in bag", status=404)


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
        return redirect('view_bag')  

    except KeyError:
        return redirect('view_bag')  
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)