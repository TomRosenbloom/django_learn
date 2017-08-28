from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from . import forms
from .forms import SignUpForm, ProfileForm
from backend.models import Profile

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password) # this is going to check these credentials against db
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('vol_reg:index'))
            else:
                return HttpResponse("Account not active")
        else:
            print("Failed login")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("invalid login")
    else:
        return render(request,'vol_reg/user_login.html',{})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('vol_reg:index'))


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            Profile.objects.create(user_id=user.pk,is_volunteer=True)

            return redirect('vol_reg:profile')
    else:
        form = SignUpForm()
    return render(request, 'vol_reg/signup.html', {'form': form})


@login_required
def profile(request):

    import logging
    logging.basicConfig(filename='mylog.log', level=logging.DEBUG)

    user = request.user
    profile = user.profile

    form = ProfileForm(instance=profile)

    if request.method == 'POST':

        logging.debug('post data received from form')

        form = ProfileForm(request.POST,instance=profile)

        #logging.debug('form=%s', form)
        logging.debug(request.POST)

        if form.is_valid():
            logging.debug(form.cleaned_data.get('activitys')) # <TreeQuerySet [<Activity: Building Work>, <Activity: Gardening>]>
            profile = form.save(commit=False)
            profile.user_id = request.user.id
            profile.activitys = form.cleaned_data.get('activitys')
            profile.save()

    return render(request,'vol_reg/profile.html', {'form': form})


def index(request):
    return render(request,'vol_reg/index.html')
