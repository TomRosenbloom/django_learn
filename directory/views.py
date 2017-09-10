from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from backend.models import Organisation

# Create your views here.

class OrganisationListView(ListView):
    context_object_name = 'organisations'
    model = Organisation
    template_name = 'directory/organisation_list.html'

class OrganisationDetailView(DetailView):
    context_object_name = 'organisation_detail'
    model = Organisation
    template_name = 'directory/organisation_detail.html'

class IndexView(TemplateView):
    template_name = 'directory/index.html'
