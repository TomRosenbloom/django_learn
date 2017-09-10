from django.shortcuts import render
from django.views.generic import View, TemplateView, FormView
from . import forms
from .forms import OrganisationForm
from backend.models import OrganisationType, Organisation

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

class OrgSignUpView(TemplateView):
    template_name = 'org_reg/signup.html'

class IndexView(TemplateView):
    template_name = 'org_reg/index.html'
