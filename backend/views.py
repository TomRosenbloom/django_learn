from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .models import Profile

# Create your views here.

def index(request):
    user = request.user
    if hasattr(user, 'profile'):
        profile = user.profile
        is_volunteer = profile.is_volunteer
        is_org_member = profile.is_org_member
    else:
        is_volunteer = is_org_member = 0
    my_dictionary = {'is_volunteer': is_volunteer, 'is_org_member': is_org_member}
    return render(request,'backend/index.html',context=my_dictionary)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password) # this is going to check these credentials against db
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account not active")
        else:
            print("Failed login")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("invalid login")
    else:
        return render(request,'backend/user_login.html',{})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
