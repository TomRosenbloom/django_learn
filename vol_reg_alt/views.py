from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms
from .forms import UserForm, ProfileForm

from django.contrib.auth import login, authenticate

from backend.models import Profile

# Create your views here.

def index(request):
    return render(request,'vol_reg_alt/index.html')


def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()

            registered = True

        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    return render(request,'vol_reg_alt/register.html',
                            {'user_form':user_form,
                             'profile_form':profile_form,
                             'registered':registered})
