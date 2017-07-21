from django.shortcuts import render
from django.http import HttpResponse
from . import forms

from address.models import Address

from .forms import OrganisationAddrForm

# Create your views here.

def index(request):
  my_dictionary = {'insert_var':"inserted text"}
  return render(request,'backend/index.html',context=my_dictionary)

def other(request):
    other_dict = {'insert_var':"inserted text"}
    return render(request,'backend/other.html',context=other_dict)

def form_view(request):
    form = forms.FormName()

    if request.method == 'POST':
        form = forms.FormName(request.POST)
        if form.is_valid():
            print("valid")
            print(form.cleaned_data['name'])
            print(form.cleaned_data['email'])

    return render(request,'backend/form_page.html',{'form':form})


def org_addr_form(request):
    if request.method == 'POST':
        form = OrganisationAddrForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = OrganisationAddrForm(initial={'address': Address.objects.first()})
    return render(request, 'backend/org_addr_form.html', {'form': form})
