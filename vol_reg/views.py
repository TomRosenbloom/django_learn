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
from backend.models import Skill, Activity, Opportunity

from user_types.models import UserProfile, Volunteer

from utils.my_crud_utils import category_belonging_dict


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

@login_required(login_url='/volunteer/login/')
@user_passes_test(is_volunteer,login_url='/volunteer/not_authorised/')
def index(request):

    # get profile details
    user = request.user
    profile = user.userprofile.volunteer
    activities = category_belonging_dict(profile, 'activitys')
    skills = category_belonging_dict(profile, 'skills')

    # get matching opps
    print(activities)
    print(Opportunity.objects.filter(activitys__name__in=activities))
    matched_opps = []
    matched_on_activitys = Opportunity.objects.filter(activitys__name__in=activities)
    matched_on_skills = Opportunity.objects.filter(skills__name__in=skills)

    import itertools
    matched_opps = itertools.chain(matched_on_activitys, matched_on_skills)
    #matched_opps.extend(matched_on_activitys)

    opps = {}

    # https://stackoverflow.com/questions/1692388/python-list-of-dict-if-exists-increment-a-dict-value-if-not-append-a-new-dic

    # for opp in matched_opps:
    #     print(opp)
    #     if not opp in opps:
    #         opps[opp] = 1
    #     else:
    #         opps[opp] += 1

    # from collections import defaultdict
    #
    # opps = defaultdict(int)
    # for opp in matched_opps:
    #     opps[opp] += 1

    from collections import Counter

    opps = Counter(matched_opps)

    print(opps)



    # would be cool to specify the reason(s) for the match
    # - this would also be a route to ordering them i.e. if there is more than one reason for the match
    # to do this you'd need to a query for each possible match case i.e. currently
    # skill, activity, or location, rather than combining these in a single big query
    # (you probably could do a single query that does all this and groups results
    # according to why matched but I wouldn't think that's a good way of doing it -
    # for the price of extra database hits, better to have it clearer in the code)
    # So...
    # what we want to hand to the template is a list of opportunities, with, for each
    # one, one or more reason for the match (your skill 'financial management',
    # your activities gardening and building etc)
    # so that's going to be a multidimensional array:
    # for each opp, for each type of match, the matches
    # How would you order that? Number of matches seems obvious, and you could weight
    # some types of match more than others, but this calculation would have to be done
    # in the view and then supplied to the template, so that would need someting else
    # added to the data array (do this as json?)
    # Aha - I can make matches a model right? Hmmm, perhaps not. Opportunity is the model.
    # I might define matches as a property of that model and put the functionality
    # with the Opportunity class... It is intersting though - you can look at matches from
    # different perspective, by user, by opp, by org, so it could be useful to have
    # it really defined in a class. But you wouldn't want it in a database table right? No,
    # because you do want it re-calculated on the fly every time the user refreshes
    #
    # Anyway, how am I going to construct this array (or whatever)...
    # It will have to be a two stage process, I would think, first pass to find matches
    # for each criterion, second path to aggregate that data i.e. pull together matches
    # of each type for each opp
    # Is there a better way?
    # construct list of zeroes of length=number of opps then increment the index of the opp id, then order on value

    return render(request,'vol_reg/index.html', {
        'profile': profile,
        'activities': activities,
        'matched_opps': matched_on_activitys # temp, to prevent errors
        #'matched_opps': matched_opps
        })
