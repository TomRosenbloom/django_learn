from django.shortcuts import render, redirect
from django.views.generic import (View, TemplateView, FormView,
                                ListView, DetailView, CreateView,
                                UpdateView, DeleteView)
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from . import forms
from .forms import SignUpForm, ProfileForm, UserForm
from backend.models import Skill, Activity, Opportunity

from user_types.models import UserProfile, Volunteer, Org_user

from utils.my_crud_utils import category_belonging_dict
from utils.my_location_utils import postcode_lookup, postcodes_in_radius


def is_volunteer(user):
    if hasattr(user, 'userprofile'):
        profile = user.userprofile
        if hasattr(profile, 'volunteer'):
            result = 1
        else:
            result = 0
    else:
        result = 0
    return result == 1

# Create your views here.

class VolLogin(TemplateView):
    template_name = 'vol_reg/vol_login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
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
    def get(self, request, *args, **kwargs):
            return render(request,'vol_reg/vol_login.html',{})


class VolLogout(LoginRequiredMixin, View):
    def get(self, request):
        username = request.user.username
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Logged out ' + username)
        return HttpResponseRedirect(reverse('vol_reg:index'))

class NotAuthorised(TemplateView):
    template_name = 'vol_reg/not_authorised.html'


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            Volunteer.objects.create(user_id=user.pk)
            messages.add_message(request, messages.INFO, 'Thanks for signing up, now you can edit your profile')
            return redirect('vol_reg:profile')
    else:
        form = SignUpForm()
    return render(request, 'vol_reg/signup.html', {'form': form})



@login_required(login_url='/volunteer/not_authorised/')
@user_passes_test(is_volunteer,login_url='/volunteer/not_authorised/')
def profile(request):

    user = request.user
    profile = user.userprofile.volunteer
    form = ProfileForm(instance=profile) # why do this here rather than following 'else' of 'if POST'?
    userForm = UserForm(instance=user)

    import mptt
    activityDict = category_belonging_dict(profile, 'activitys')
    skillDict = category_belonging_dict(profile, 'skills')

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        userForm = UserForm(request.POST, instance=user)

        if form.is_valid() and userForm.is_valid():
            user = userForm.save()
            profile = form.save(commit=False)
            profile.user_id = request.user.id
            profile.activitys = form.cleaned_data.get('activitys')
            profile.skills = form.cleaned_data.get('skills')
            profile.save()
            return redirect('vol_reg:index')

    return render(request,'vol_reg/profile.html', {
    'form': form,
    'userForm': userForm,
    'allActivities': Activity.objects.all(),
    'profileActivities': activityDict,
    'allSkills': Skill.objects.all(),
    'profileSkills': skillDict
    })

@login_required(login_url='/volunteer/login/')
@user_passes_test(is_volunteer,login_url='/volunteer/not_authorised/')
def index(request):

    # get profile details
    user = request.user
    profile = user.userprofile.volunteer
    activities = category_belonging_dict(profile, 'activitys')
    skills = category_belonging_dict(profile, 'skills')

    # get matching opps
    matched_opps = []
    matched_on_activitys = Opportunity.objects.filter(activitys__name__in=activities)
    matched_on_skills = Opportunity.objects.filter(skills__name__in=skills)

    # location/range matches:
    postcode_data = postcode_lookup(profile.postcode)
    if postcode_data['status'] == 200 and postcode_data['result']['longitude'] and postcode_data['result']['latitude']:
        postcodes_in_range = postcodes_in_radius((profile.range*1.61),postcode_data['result']['latitude'],postcode_data['result']['longitude'])
        matched_on_range = Opportunity.objects.filter(organisation__postcode__in=postcodes_in_range)
        # need a way to signal that there was a match on postcode

    # aggregate matches of different types into a single array of matches
    import itertools
    all_matches = itertools.chain(matched_on_activitys, matched_on_skills, matched_on_range)

    # for match in all_matches:
    #     print(match.organisation.postcode)



    # make a count of matches per opp - note this will include not just the count but the details of each match
    all_match_counts = {}
    from collections import Counter
    all_match_counts = Counter(all_matches).most_common() # most_common sorts on count value

    postcode_list = []
    for postcode in postcodes_in_range:
        postcode_list.append(postcode.postcode)

    return render(request,'vol_reg/index.html', {
        'profile': profile,
        'activities': activities,
        'skills': skills,
        'all_match_counts': all_match_counts,
        'postcodes_in_range': postcode_list
        })


def test(request):
#     from utils.my_location_utils import postcode_lookup, distance, square_around_origin, places_in_square, places_in_circle
#     print(distance(0,0,20,20))
#     print(square_around_origin(8,50.740201781113,-3.60225065630703))
#     print(square_around_origin(8,50.740201781113,-3.60225065630703)[1]) #prints the values in the tuple returned by function
#     places_square = places_in_square(square_around_origin(1,50.740201781113,-3.60225065630703))
#     places_circle = places_in_circle(places_in_square(square_around_origin(1,50.740201781113,-3.60225065630703)),50.740201781113,-3.60225065630703,1)
#     print(len(places_square))
#     print(len(places_circle))
    from backend.models import Postcode
    postcode = Postcode.objects.filter(id=5)
    print(postcode)
    return render(request,'vol_reg/test.html')
