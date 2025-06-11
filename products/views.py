from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm


def all_products(request):
    """ A view to show all products, including sorting and search queries """
    products = Product.objects.all().order_by('category')
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            if sortkey == 'name':
                sort = 'name'
                products = products.order_by(sort)
            elif sortkey == 'category':
                sort = 'category'
                products = products.order_by(sort)
            elif sortkey == 'price':
                sort = 'price'
                products = products.order_by(sort)
            else:
                sort = 'name'
                products = products.order_by(sort)

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sort = f'-{sort}'
                    products = products.order_by(sort)
                else:
                    sort = f'{sort}'
                    products = products.order_by(sort)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if request.GET:
            if 'q' in request.GET:
                query = request.GET['q']
                if not query:
                    messages.error(
                        request, "You didn't enter any search criteria!"
                    )
                    return redirect(reverse('products'))
                queries = Q(name__icontains=query) | Q(
                    description__icontains=query)
                products = products.filter(queries)

    current_sorting = f'{sort}_{direction}' if sort else 'name_asc'

    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/products.html', {
        'products': page_obj.object_list,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        'page_obj': page_obj
    })

# product detail view
def product_detail(request, product_id):
    """ A view to show a single product detail page """
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/product_detail.html',
                  {'product': product})


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Only store owners can add products.')
        return redirect(reverse('home'))
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product added successfully!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request,
                'Failed to add product. Please ensure the form is valid.'
            )
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Only store owners can edit products.')
        return redirect(reverse('home'))
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request, 'Failed to update product. '
                'Please ensure the form is valid.'
            )
    else:
        form = ProductForm(instance=product)

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Only store owners can delete products.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        product.delete()
        messages.success(
            request, f'Product "{product.name}" has been deleted successfully!'
        )
        return redirect(reverse('products'))

    template = 'products/product_confirm_delete.html'
    context = {
        'product': product,
    }

    return render(request, template, context)
