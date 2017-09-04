from django.shortcuts import render

# Create your views here.

def org_login(request):
    return render(request,'org_reg/org_login.html')

def profile(request):
    return render(request,'org_reg/profile.html')

def signup(request):
    return render(request,'org_reg/signup.html')

def index(request):
    return render(request,'org_reg/index.html')
