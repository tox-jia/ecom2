from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Product, Category, Profile, Membership
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import UpdateUserForm, UserInfoForm
# from .forms import ChangePasswordForm, SignUpForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django import forms
from django.db.models import Q
# //this is to search description by using Django Q (maybe for query)
import json
# // json = javascript object notation, like python dictionary in javascript form
from cart.cart import Cart
from blog.models  import BlogPost





def card(request):
    return render(request, "card.html", {})


def search(request):
    # determine if the user filled out the form
    if request.method == "POST":
        searched = request.POST['searched']
        # get the input box 'searched' in html: <input ... name="searched">

        # let's query the DB model of Products
        searched = Product.objects.filter(Q(name__icontains=searched) |
                                          Q(description__icontains=searched))
        # // icontains = search CASE insensitive, 'contain' P & p will be different
        # // use '|' for or
        # // use 'Q()' for multiple query tasks

        # test for null
        if not searched:
            messages.success(request, "Not exist")
            return render(request, "search.html", {})
        else:
            return render(request, "search.html", {'searched':searched})
    else:
        return render(request, "search.html", {})


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        # get the current user's shipping info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # // why use 'user__id' is because: the time we build the code, we created the user first, the shipping address
        # // is added later, so the ids won't match the reality. for example, the admin as the id 1, but tom as id 2
        # // may be the frist to create the shippingaddress page.
        # Get original User Form, create the form
        form = UserInfoForm(request.POST or None, instance=current_user)
        # get user's shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        # if there is POST, then execute the form; if not, create an instance
        # with the current user having username, first name, second name, and email
        if form.is_valid() or shipping_form.is_valid():
            # save original form
            form.save()
            # save shipping form
            shipping_form.save()
            messages.success(request, "Info Updated")
            return redirect('update_info')
        return render(request, "update_info.html", {'form':form, 'shipping_form':shipping_form})
    else:
        messages.danger(request, "You Must Be Logged In")
        return redirect('home')


# def update_password(request):
#     if request.user.is_authenticated:
#         concurrent_user = request.user
#         # Did they fill out the form
#         if request.method == 'POST':
#             form = ChangePasswordForm(concurrent_user, request.POST)
#             # is the form valid
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, "Password Updated")
#                 login(request, concurrent_user)
#                 return redirect('home')
#             else:
#                 for error in list(form.errors.values()):
#                     messages.error(request, error)
#                     return redirect('update_password')
#         else:
#             form = ChangePasswordForm(concurrent_user)
#             return render(request, "update_password.html", {'form': form})
#     else:
#         messages.danger(request, "Must Logged in")


def update_user(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        # create form
        user_form = UpdateUserForm(request.POST or None, instance=profile)
        # if there is POST, then execute the form; if not, create an instance
        # with the current user having username, first name, second name, and email
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Updated")
            return redirect('update_user')
        return render(request, "update_user.html", {'user_form':user_form})
    else:
        messages.danger(request, "You Must Be Logged In")
        return redirect('home')


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories":categories})


def category(request,foo):
    foo = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success(request, ("Category doesn't exit"))
        return redirect('home')


def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})


def membership(request):
    memberships = Membership.objects.all()
    return render(request, 'membership.html', {'memberships':memberships})


def home(request):
    blogposts = BlogPost.objects.all().order_by('-date_created')
    return render(request, 'home.html', {
        'blogposts': blogposts,
    })


def about(request):
    return render(request, 'about.html', {
    })


# def login_user(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#
#             # do some shopping cart stuff
#             current_user = Profile.objects.get(user__id=request.user.id)
#             # get their saved cart from DB
#             saved_cart = current_user.old_cart
#             # convert DB string to python dictionary
#             if saved_cart:
#                 # convert to dictionary using JSON
#                 # {"3":2} to {'3':2}
#                 converted_cart = json.loads(saved_cart)
#                 # add the loaded dictionary to our session
#                 cart = Cart(request)
#                 # loop through the Cart and add the items from the DB
#                 for key,value in converted_cart.items():
#                     cart.db_add(product=key, quantity=value)
#
#             messages.success(request, ('Logged In!'))
#             return redirect('home')
#     else:
#         return render(request, 'login.html', {})


def google_login_redirect(request):
    return redirect('/accounts/google/login/')


def logout_user(request):
    logout(request)
    messages.success(request, ('Logged Out!'))
    return redirect('home')


# def register_user(request):
#     form = SignUpForm()
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             # log in User
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             messages.success(request, ('Registered'))
#             return redirect('update_info')
#         else:
#             messages.success(request, ('error'))
#             return redirect('register')
#     else:
#         return render(request, 'register.html', {'form':form})