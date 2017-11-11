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

from . import forms
from .forms import SignUpForm, ProfileForm
from backend.models import Skill, Activity

from user_types.models import UserProfile, Volunteer

from utils.my_crud_utils import category_belonging_dict

# this method, using groups, is defunct
# def is_volunteer(user):
#     return user.groups.filter(name__in=['volunteer',]).exists()
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
        logout(request)
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

            # g = Group.objects.get(name='volunteer')
            # g.user_set.add(user)

            return redirect('vol_reg:profile')
    else:
        form = SignUpForm()
    return render(request, 'vol_reg/signup.html', {'form': form})


#
# put this aside for now: 'Generic detail view ProfileUpdateView must be called with either an object pk or a slug'
#
# class ProfileUpdateView(LoginRequiredMixin, UpdateView):
#     fields = ('postcode','range','skills','activitys')
#     model = UserProfile
#     template_name = 'vol_reg/profile.html'
#     success_url = reverse_lazy('vol_reg:profile')
#
#     def get_context_data(self, **kwargs):
#         context = super(ProfileUpdateView, self).get_context_data(**kwargs)
#         user = request.user
#         print('foo')
#         profile = user.userprofile.volunteer
#         context['profileActivities'] = category_belonging_dict(profile, 'activitys')
#         context['allActivities'] = Activity.objects.all()
#         context['profileSkills'] = category_belonging_dict(profile, 'skills')
#         context['allSkills'] = Skill.objects.all()
#         return context
#
#     class Meta:
#         labels = {
#             'range': 'Travel range',
#             'activitys': 'Activities'
#         }

@login_required(login_url='/volunteer/not_authorised/')
@user_passes_test(is_volunteer,login_url='/volunteer/not_authorised/')
def profile(request):

    user = request.user
    #profile = user.profile
    profile = user.userprofile.volunteer
    form = ProfileForm(instance=profile)

    import mptt
    # obvs need to make a function of some sort here as I am repeating myself
    activityDict = category_belonging_dict(profile, 'activitys')
    skillDict = category_belonging_dict(profile, 'skills')

    if request.method == 'POST':
        form = ProfileForm(request.POST,instance=profile)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user_id = request.user.id
            profile.activitys = form.cleaned_data.get('activitys')
            profile.skills = form.cleaned_data.get('skills')
            profile.save()
            return redirect('vol_reg:profile')

    return render(request,'vol_reg/profile.html', {
    'form': form,
    'allActivities': Activity.objects.all(),
    'profileActivities': activityDict,
    'allSkills': Skill.objects.all(),
    'profileSkills': skillDict
    })


def index(request):
    return render(request,'vol_reg/index.html')
