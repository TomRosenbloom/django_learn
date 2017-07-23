from django.shortcuts import render
from django.http import HttpResponse
from . import forms
from .forms import RegForm

# Create your views here.

def index(request):
    return render(request,'vol_reg/index.html')


def register(request):
    return render(request,'vol_reg/register.html')


def registration_form(request):
    form = RegForm()
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return register(request)
        else:
            print("ERROR")
    return render(request,'vol_reg/reg_form.html',{'form':form})
