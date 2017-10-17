from django.shortcuts import render, redirect
from django.views.generic import (View, TemplateView, FormView,
                                ListView, DetailView, CreateView,
                                UpdateView, DeleteView)
from django import forms

#from . import forms
from .forms import OrganisationForm, SignUpForm, OpportunityForm

from backend.models import OrganisationType, Organisation, Opportunity

from user_types.models import Org_user
from user_types.models import UserProfile

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, AccessMixin


def org_user_check(user):
    if hasattr(user, 'userprofile'):
        profile = user.userprofile
        if hasattr(profile, 'org_user'):
            is_org_member = 1
        else:
            is_org_member = 0
    else:
        is_org_member = 0
    return is_org_member == 1


# Create your views here.

class OpportunityDeleteView(DeleteView):
    model = Opportunity
    template_name = 'org_reg/opportunity_confirm_delete.html'
    success_url = reverse_lazy('org_reg:index')


class OpportunityUpdateView(UpdateView):
    fields = ('name','description','start_date','end_date')
    model = Opportunity
    template_name = 'org_reg/opportunity_form.html'
    success_url = reverse_lazy('org_reg:index')

    class Meta:
        labels = {
            'name': 'Opportunity title'
        }

class OpportunityCreateView(CreateView):
    fields = ('name','description','start_date','end_date')
    model = Opportunity
    template_name = 'org_reg/opportunity_form.html'

    def get_context_data(self, **kwargs):
        context = super(OpportunityCreateView, self).get_context_data(**kwargs)
        context['organisation'] = Organisation.objects.get(pk=self.kwargs['organisation'])
        return context

    def form_valid(self, form, **kwargs):
        opportunity = form.save(commit=False)
        opportunity.organisation = Organisation.objects.get(pk=self.kwargs['organisation'])
        #return HttpResponse(form.instance.start_date) # coming as yyy-mm-dd
        return super(OpportunityCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('org_reg:index')

    class Meta:
        labels = {
            'name': 'Opportunity title'
        }

class OrganisationSelect(View):

    def post(self, request, *args, **kwargs):
        organisation = request.POST.get('organisation')
        # use the current user, or send in form?
        user = request.user
        user.userprofile.org_user.organisations.add(organisation)
        return redirect('org_reg:index')

    def get(self, request):
        return render(request, 'org_reg/organisation_select.html', {'organisations': Organisation.objects.all()})

class OrganisationDetailView(DetailView):
    context_object_name = 'organisation_detail'
    model = Organisation
    template_name = 'org_reg/organisation_detail.html'

class OrganisationCreateView(CreateView):
    fields = ('name','aims_and_activities','postcode','email','telephone')
    model = Organisation
    template_name = 'org_reg/organisation_form.html'

    def form_invalid(self, form):
        print(form.errors)



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
    #success_message = "%(name)s was deleted"

class ProfileView(FormView):
    form_class = OrganisationForm
    template_name = 'org_reg/profile.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = OrganisationType.objects.all()
        return context


class OrgLogin(TemplateView):
    template_name = 'org_reg/org_login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                #is_org_user = org_user_check(user)
                if org_user_check(user):
                    login(request,user)
                    return HttpResponseRedirect(reverse('org_reg:index'))
                else:
                    messages.error(request, 'You have not registered as an organisational user')
            else:
                messages.error(request, 'Account not active')
        else:
            messages.error(request, 'Incorrect username or password')
        return render(request,'org_reg/org_login.html')

    def get(self, request, *args, **kwargs):
            return render(request,'org_reg/org_login.html',{})


class OrgLogout(LoginRequiredMixin, View):
    def get(self, request):
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
            Org_user.objects.create(user_id=user.pk)

            return redirect('org_reg:index')
        else:
            return render(request, 'org_reg/signup.html', {'form': form})

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'org_reg/signup.html', {'form': form})


class IndexView(UserPassesTestMixin,TemplateView):
    template_name = 'org_reg/index.html'
    login_url = 'login/'

    def get(self, request, *args, **kwargs):
        orgs = request.user.userprofile.org_user.organisations.all
        return render(request, 'org_reg/index.html', {'orgs': orgs})

    def test_func(self):
        return org_user_check(self.request.user)
