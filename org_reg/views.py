from django.shortcuts import render
from . import forms
from .forms import OrganisationForm
from backend.models import OrganisationType

# Create your views here.

def org_login(request):
    return render(request,'org_reg/org_login.html')

def profile(request):
    form = OrganisationForm()
    return render(request, 'org_reg/profile.html', {'form': form, 'types': OrganisationType.objects.all()})

def signup(request):
    return render(request,'org_reg/signup.html')

def index(request):
    return render(request,'org_reg/index.html')
