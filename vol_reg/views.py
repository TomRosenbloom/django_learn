from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView

from . import forms
from .forms import SignUpForm, ProfileForm
from backend.models import Skill, Activity

from user_types.models import Volunteer

# Create your views here.


def is_volunteer(user):
    return user.groups.filter(name__in=['volunteer',]).exists()

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

            g = Group.objects.get(name='volunteer')
            g.user_set.add(user)

            return redirect('vol_reg:profile')
    else:
        form = SignUpForm()
    return render(request, 'vol_reg/signup.html', {'form': form})



@login_required
@user_passes_test(is_volunteer)
def profile(request):

    user = request.user
    #profile = user.profile
    profile = user.userprofile.volunteer
    form = ProfileForm(instance=profile)

    import mptt
    # obvs need to make a function of some sort here as I am repeating myself
    activityDict = {}
    activities = mptt.utils.tree_item_iterator(profile.activitys.all(), ancestors=False)
    for activity in activities:
        activityDict[activity[0].name] = activity[0].name

    skillDict = {}
    skills = mptt.utils.tree_item_iterator(profile.skills.all(), ancestors=False)
    for skill in skills:
        skillDict[skill[0].name] = skill[0].name

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
