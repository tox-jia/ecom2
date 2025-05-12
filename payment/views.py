from django.shortcuts import render, redirect
from django.contrib import messages
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItems
from django.contrib.auth.models import User
from store.models import Product, Profile
import datetime


def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # Get the order
        order = Order.objects.get(id=pk)
        # get the order items
        items = OrderItems.objects.filter(order=pk)

        if request.POST:
            order = Order.objects.filter(id=pk)
            status = request.POST['shipping_status']
            if status == "true":
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                order.update(shipped=False)
            messages.success(request, "Shipping Status Updated")
            return redirect('shipped_dash')

        return render(request, "payment/orders.html", {'order':order, 'items':items})
    else:
        messages.success(request, ('Access Denied'))
        return redirect('home')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)

        if request.POST:
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            now = datetime.datetime.now()
            order.update(shipped=True, date_shipped=now)
            messages.success(request, "Shipping Status Updated")
            return redirect('shipped_dash')

        return render(request, "payment/not_shipped_dash.html", {'orders':orders})
    else:
        messages.success(request, ('Access Denied'))
        return redirect('home')


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)

        if request.POST:
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            order.update(shipped=False)
            messages.success(request, "Shipping Status Updated")
            return redirect('not_shipped_dash')

        return render(request, "payment/shipped_dash.html", {'orders': orders})
    else:
        messages.success(request, ('Access Denied'))
        return redirect('home')


def process_order(request):
    # get the cart
    cart = Cart(request)
    cart_products = cart.get_pros()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    if request.POST:
        # get billing_info from the last page
        payment_form = PaymentForm(request.POST or None)
        # Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')

        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        # create shipping address from session info
        shipping_address = (f"{my_shipping['shipping_address1']}\n"
                            f"{my_shipping['shipping_address2']}\n"
                            f"{my_shipping['shipping_city']}\n"
                            f"{my_shipping['shipping_state']}\n"
                            f"{my_shipping['shipping_zipcode']}\n"
                            f"{my_shipping['shipping_country']}\n")
        amount_paid = totals
        # create an order
        if request.user.is_authenticated:
            # logged in
            user = request.user
            create_order = Order(user=user, full_name=full_name, email=email,
                                 shipping_address=shipping_address,
                                 amount_paid=amount_paid)
            create_order.save()

            # add order items
            # get the order id
            order_id = create_order.pk
            #// pk stands for primary Key

            # get product Info
            for product in cart_products:
                # get product id
                product_id = product.id
                # get product price
                if product.is_sale:
                    price = product.is_sale
                else:
                    price = product.price
                # get quantity
                for key,value in quantities.items():
                    if int(key) == product.id:
                        # create order item
                        create_order_item = OrderItems(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()

        else:
            # not logged in
            create_order = Order(full_name=full_name, email=email,
                                 shipping_address=shipping_address,
                                 amount_paid=amount_paid)
            # // no 'user' because it is guest mode
            create_order.save()
            # add order items
            # get the order id
            order_id = create_order.pk
            # // pk stands for primary Key

            # get product Info
            for product in cart_products:
                # get product id
                product_id = product.id
                # get product price
                if product.is_sale:
                    price = product.is_sale
                else:
                    price = product.price
                # get quantity
                for key, value in quantities.items():
                    if int(key) == product.id:
                        # create order item
                        create_order_item = OrderItems(order_id=order_id, product_id=product_id,
                                                       quantity=value, price=price)
                        create_order_item.save()

        # clean the cart
        for key in list(request.session.keys()):
            if key == 'session_key':
                # delete the key
                del request.session[key]
            # also clean & update DB where the cart previous history was saved
            if request.user.is_authenticated:
                clear_cart_profile = Profile.objects.filter(user__id=request.user.id)
                clear_cart_profile.update(old_cart={})
        messages.success(request, ('Order Placed'))
        return redirect('home')

    else:
        messages.success(request, ('Access Denied'))
        return redirect('home')



def billing_info(request):
    if request.POST:
        # get the cart
        cart = Cart(request)
        cart_products = cart.get_pros()
        quantities = cart.get_quants()
        totals = cart.cart_total()

        # create a session with shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # check to see if the user is logged in
        if request.user.is_authenticated:
            # Get the Billing Form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products": cart_products,
                                                                 "quantities": quantities,
                                                                 "totals": totals,
                                                                 "shipping_info": request.POST,
                                                                 "billing_form":billing_form})
        else: # if not logged in
            # Get the Billing Form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products": cart_products,
                                                                 "quantities": quantities,
                                                                 "totals": totals,
                                                                 "shipping_info": request.POST,
                                                                 "billing_form": billing_form})
    else:
        messages.success(request, ('Access Denied'))
        return redirect('home')


def checkout(request):
    # get the cart
    cart = Cart(request)
    cart_products = cart.get_pros()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    if request.user.is_authenticated:
    # checkout as logged in user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, "payment/checkout.html", {"cart_products": cart_products,
                                                         "quantities": quantities,
                                                         "totals": totals,
                                                         "shipping_form":shipping_form})
    # checkout as guest
    else:
        shipping_form = ShippingForm(request.POST or None)
        # // here we don't need instance as intance is where we pipe in the saved information
        return render(request, "payment/checkout.html", {"cart_products": cart_products,
                                                         "quantities": quantities,
                                                         "totals": totals,
                                                         "shipping_form":shipping_form})


def payment_success(request):
    return render(request, 'payment/payment_success.html', {})

