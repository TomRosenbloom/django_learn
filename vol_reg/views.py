from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms
from .forms import SignUpForm, ProfileForm

from django.contrib.auth import login, authenticate

from backend.models import Profile

# Create your views here.

def index(request):
    return render(request,'vol_reg/index.html')

def welcome(request):
    return render(request,'vol_reg/welcome.html') # this needs to be conditional on sign up

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # so here I want to create a minimal profile record with is_volunteer = true
            # profile model/table has foreign key user_id, so I suppose get the user id just created...
            # that should be accessible as user.pk from user = form.save(), or form.pk?
            Profile.objects.create(user_id=user.pk,is_volunteer=True)

            return redirect('vol_reg:welcome') 
    else:
        form = SignUpForm()
    return render(request, 'vol_reg/signup.html', {'form': form})

def profile(request):
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=True)

    return render(request,'vol_reg/profile.html', {'form': form})

# def register(request):
#     return render(request,'vol_reg/register.html')

# def registration_form(request):
#     form = RegForm()
#     if request.method == 'POST':
#         form = RegForm(request.POST)
#         if form.is_valid():
#             #print('foo')
#             instance = form.save(commit=True)
#             instance.is_volunteer = True
#             instance.save()
#             return register(request)
#         else:
#             print("ERROR")
#     return render(request,'vol_reg/reg_form.html',{'form':form})
