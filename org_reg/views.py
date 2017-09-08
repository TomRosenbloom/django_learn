from django.shortcuts import render
from django.views.generic import View, TemplateView, FormView
from . import forms
from .forms import OrganisationForm
from backend.models import OrganisationType

# Create your views here.

class Foo(TemplateView):
    template_name = 'org_reg/foo.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['foo'] = 'foo'
        return context

def org_login(request):
    return render(request,'org_reg/org_login.html')

class ProfileView(FormView):
    form_class = OrganisationForm
    template_name = 'org_reg/profile.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = OrganisationType.objects.all()
        return context

# def profile(request):
#     form = OrganisationForm()
#     return render(request, 'org_reg/profile.html', {'form': form, 'types': OrganisationType.objects.all()})

def signup(request):
    return render(request,'org_reg/signup.html')

def index(request):
    return render(request,'org_reg/index.html')
