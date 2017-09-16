from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from backend.models import Organisation
from .filters import OrganisationFilter

# Create your views here.

def search(request):
    org_list = Organisation.objects.all()
    org_filter = OrganisationFilter(request.GET, queryset = org_list)
    return render(request, 'directory/organisation_filter.html', {'filter': org_filter})

class OrganisationListView(ListView):
    context_object_name = 'organisations'
    model = Organisation
    template_name = 'directory/organisation_list.html'
    paginate_by = 5

class OrganisationDetailView(DetailView):
    context_object_name = 'organisation_detail'
    model = Organisation
    template_name = 'directory/organisation_detail.html'

class IndexView(TemplateView):
    template_name = 'directory/index.html'
