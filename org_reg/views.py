from django.shortcuts import render, redirect
from django.views.generic import (View, TemplateView, FormView,
                                ListView, DetailView, CreateView,
                                UpdateView, DeleteView)
from . import forms
from .forms import OrganisationForm, SignUpForm
from backend.models import OrganisationType, Organisation, Profile


from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.auth.mixins import UserPassesTestMixin

# Create your views here.

class OrganisationDetailView(DetailView):
    context_object_name = 'organisation_detail'
    model = Organisation
    template_name = 'org_reg/organisation_detail.html'

class OrganisationCreateView(CreateView):
    fields = ('name','aims_and_activities','postcode','email','telephone')
    model = Organisation
    template_name = 'org_reg/organisation_form.html'
    def get_success_url(self):
        return reverse('org_reg:detail',kwargs={'pk':self.object.pk})

class OrganisationUpdateView(UpdateView):
    fields = ('name','aims_and_activities','postcode','email','telephone')
    model = Organisation
    template_name = 'org_reg/organisation_form.html'
    def get_success_url(self):
        return reverse('org_reg:detail',kwargs={'pk':self.object.pk})

class OrganisationDeleteView(DeleteView):
    model = Organisation
    template_name = 'org_reg/organisation_confirm_delete.html'
    success_url = reverse_lazy('org_reg:list')

class ProfileView(FormView):
    form_class = OrganisationForm
    template_name = 'org_reg/profile.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = OrganisationType.objects.all()
        return context

def org_user_check(user):
    if hasattr(user, 'profile'):
        profile = user.profile
        is_org_member = profile.is_org_member
    else:
        is_org_member = 0
    return is_org_member == 1


def org_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        # check if volunteer/org user
        if hasattr(user, 'profile'):
            profile = user.profile
            is_volunteer = profile.is_volunteer
            is_org_member = profile.is_org_member
        else:
            is_volunteer = is_org_member = 0

        if user and is_org_member:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('org_reg:index'))
            else:
                return HttpResponse("Account not active")
        else:
            if is_volunteer and not is_org_member:
                messages.add_message(
                    request, messages.ERROR, "Volunteer trying to log in as org user"
                    )
            else:
                messages.add_message(
                    request, messages.ERROR, "Incorrect username or password"
                    )
            return HttpResponseRedirect(reverse( 'org_reg:login' ))
    else:
        return render(request,'org_reg/org_login.html',{})

@login_required
def org_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('org_reg:index'))

class OrgSignUpView(TemplateView):
    template_name = 'org_reg/signup.html'
    def post(self, request, *args, **kwargs):

        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            Profile.objects.create(user_id=user.pk,is_org_member=True)

            return redirect('org_reg:index')
        else:
            return render(request, 'org_reg/signup.html', {'form': form})

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'org_reg/signup.html', {'form': form})


# class IndexView(UserPassesTestMixin,TemplateView):
#     template_name = 'org_reg/index.html'
#     def test_func(self):
#         return False

@user_passes_test(org_user_check, login_url='login/')
#@permission_required()
def index(request):
    return render(request,'org_reg/index.html')
