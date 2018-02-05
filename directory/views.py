from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from backend.models import Organisation, Opportunity
from .filters import OrganisationFilter, OpportunityFilter
import django_filters
from filters.views import FilterMixin
import csv
# Create your views here.

def export_organisations_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="organisations.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Aims and activities', 'Postcode', 'Email address'])

    organisations = Organisation.objects.all().values_list('name', 'aims_and_activities', 'postcode', 'email')
    for organisation in organisations:
        writer.writerow(organisation)

    return response

class OpportunityFilterView(FilterMixin, django_filters.views.FilterView):
    filterset_class = OpportunityFilter
    context_object_name = 'opportunities'
    model = Opportunity
    template_name = 'directory/opportunity_filter.html'
    paginate_by = 10

class OpportunityDetailView(DetailView):
    context_object_name = 'opportunity_detail'
    model = Opportunity
    template_name = 'directory/opportunity_detail.html'

class OrganisationFilterView(FilterMixin, django_filters.views.FilterView):
    filterset_class = OrganisationFilter
    context_object_name = 'organisations'
    model = Organisation
    template_name = 'directory/organisation_filter.html'
    paginate_by = 5


class OrganisationListView(ListView):
    context_object_name = 'organisations'
    model = Organisation
    template_name = 'directory/organisation_list.html'
    paginate_by = 5


class OrganisationDetailView(DetailView):
    context_object_name = 'organisation_detail'
    model = Organisation
    template_name = 'directory/organisation_detail.html'

    def get_context_data(self, **kwargs):
        context = super(OrganisationDetailView, self).get_context_data(**kwargs)
        if 'opp_id' in self.kwargs:
            context['highlighted_opp'] = Opportunity.objects.get(pk=self.kwargs['opp_id'])
            # context['highlighted_opp'] = self.kwargs['opp_id']
            print(type(self.kwargs['opp_id']))
        return context


class IndexView(TemplateView):
    template_name = 'directory/index.html'
