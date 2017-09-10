from django.shortcuts import render
from django.views.generic import View, TemplateView, FormView
from . import forms
from .forms import OrganisationForm
from backend.models import OrganisationType, Organisation


from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.

class ProfileView(FormView):
    form_class = OrganisationForm
    template_name = 'org_reg/profile.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = OrganisationType.objects.all()
        return context


class OrgLoginView(TemplateView):
    template_name = 'org_reg/org_login.html'

@login_required
def org_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('org_reg:index'))

class OrgSignUpView(TemplateView):
    template_name = 'org_reg/signup.html'

class IndexView(TemplateView):
    template_name = 'org_reg/index.html'
