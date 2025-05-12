from django.shortcuts import render, get_object_or_404
from .cart import Cart
# add the cart class
from store.models import Product
# access product model
from django.http import JsonResponse
from django.contrib import messages
# whenever the thing is clicked, send back everything work out correctly


def cart_summary(request):
    # get the cart
    cart = Cart(request)
    cart_products = cart.get_pros()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products":cart_products,
                                                 "quantities":quantities, "totals":totals})


def cart_add(request):
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # Uppercase 'POST' is through webpage in Django
        # Lowercase 'post' is for jQuery without refreshing the webpage.
        # Get product
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        # look product in DB
        product = get_object_or_404(Product, id=product_id)
        # save to session
        cart.add(product=product, quantity=product_qty)

        # get cart quantity
        cart_quantity = cart.__len__()

        # Return response
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, ("Added"))
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        # call delete function in the cart
        cart.delete(product=product_id)

        response = JsonResponse({'product': product_id})
        messages.success(request, ("Deleted"))
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)
        response =JsonResponse({'qty':product_qty})
        messages.success(request, ("Updated"))
        return response



