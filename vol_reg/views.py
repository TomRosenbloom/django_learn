from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms
from .forms import RegForm, SignUpForm

from django.contrib.auth import login, authenticate

# Create your views here.

def index(request):
    return render(request,'vol_reg/index.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'vol_reg/signup.html', {'form': form})


def register(request):
    return render(request,'vol_reg/register.html')

def registration_form(request):
    form = RegForm()
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            #print('foo')
            instance = form.save(commit=True)
            instance.is_volunteer = True
            instance.save()
            return register(request)
        else:
            print("ERROR")
    return render(request,'vol_reg/reg_form.html',{'form':form})
