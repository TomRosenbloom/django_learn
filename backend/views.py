from django.shortcuts import render
from django.http import HttpResponse
from . import forms

from address.models import Address


# Create your views here.

def index(request):
  my_dictionary = {'insert_var':"inserted text"}
  return render(request,'backend/index.html',context=my_dictionary)
