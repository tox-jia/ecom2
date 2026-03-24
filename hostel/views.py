from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Guest
from .forms import CheckinForm
from django import forms
from django.db.models import Q
# //this is to search description by using Django Q (maybe for query)
import json
# // json = javascript object notation, like python dictionary in javascript form


def checkin(request):
    if request.method == "POST":
        form = CheckinForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()  # Save and get the BlogPost instance
            return redirect('view_guest', pk=post.pk)  # Redirect to the view_post page
        else:
            print(request.FILES)
            print(form.errors)
    else:
        form = CheckinForm()
    return render(request, 'hostel_checkin.html', {'form': form})


def viewGuest(request, pk):
    guest = get_object_or_404(Guest, pk=pk)
    return render(request, 'view_guest.html', {'guest': guest})