from django.shortcuts import render, redirect
from django.views.generic import (View, TemplateView, FormView,
                                ListView, DetailView, CreateView,
                                UpdateView, DeleteView)
from django import forms
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.forms import formset_factory
from django.db import IntegrityError, transaction
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.core import serializers
import json

from django_tables2 import SingleTableView

from backend.models import Organisation, OrganisationRegistration, Opportunity
from crm.forms import OrganisationRegistrationForm
from crm.tables import OpportunityTable, OrganisationTable

def get_org_opps(request):
    org_id = request.GET.get('org_id')
    org = Organisation.objects.get(id=org_id)
    opps = Opportunity.objects.filter(organisation=org).values('name','description')
    return HttpResponse(json.dumps(list(opps)))
    # data = serializers.serialize('json',opps)
    #return JsonResponse(opps, safe=False)

# Create your views here.

class OpportunityDeleteView(DeleteView):
    model = Opportunity
    template_name = 'crm/opportunity_confirm_delete.html'
    success_url = reverse_lazy('crm:list-opps')

class OpportunityUpdateView(UpdateView):
    fields = ('name','description','start_date','end_date')
    model = Opportunity
    template_name = 'crm/opportunity_update.html'
    success_url = reverse_lazy('crm:list-opps')

    class Meta:
        labels = {
            'name': 'Opportunity title'
        }

class OpportunityCreateView(CreateView):
    fields = ('organisation','name','description','start_date','end_date')
    model = Opportunity
    template_name = 'crm/opportunity_create.html'
    success_url = reverse_lazy('crm:list-opps')

# this is going to work a bit differently from the org_reg version
# in that case the organisation id comes via the url, but in this case
# we want org name as the first field
# (and then with an ajax look up that displays existing opps once the org is selected)



    class Meta:
        labels = {
            'name': 'Opportunity title'
        }

class OpportunityTable(SingleTableView):
    model = Opportunity
    table_class = OpportunityTable
    template_name = 'crm/opportunity_table.html'

class OpportunityListView(ListView):
    context_object_name = 'opportunities'
    model = Opportunity
    template_name = 'crm/opportunity_list.html'
    paginate_by = 10


class OrganisationTable(SingleTableView):
    model = Organisation
    table_class = OrganisationTable
    template_name = 'crm/organisation_table.html'
    table_pagination = {
        'per_page': 10
    }

class OrganisationListView(ListView):
    context_object_name = 'organisations'
    model = Organisation
    template_name = 'crm/organisation_list.html'
    paginate_by = 5


class OrganisationUpdateView(UpdateView):
    RegistrationFormset = formset_factory(OrganisationRegistrationForm, can_delete=True)
    fields = ('name','aims_and_activities','postcode','email','telephone')
    model = Organisation
    template_name = 'crm/organisation_form.html'
    success_url = reverse_lazy('crm:list')

    def get_context_data(self, **kwargs):
        context = super(OrganisationUpdateView, self).get_context_data(**kwargs)
        organisation = Organisation.objects.get(pk=self.kwargs['pk'])
        org_type_data = OrganisationRegistration.objects.filter(organisation=organisation)
        type_reg_data = [{'type':d.type, 'reg_number': d.reg_number}
                            for d in org_type_data]
        context['type_reg_formset'] = self.RegistrationFormset(initial=type_reg_data)
        return context

    def form_valid(self, form):
        organisation = form.save(commit=False)
        type_reg_formset = self.RegistrationFormset(self.request.POST)
        if type_reg_formset.is_valid():
            try:
                with transaction.atomic():
                    OrganisationRegistration.objects.filter(organisation=organisation).delete()
                    for type_reg_form in type_reg_formset:
                        type = type_reg_form.cleaned_data.get('type')
                        reg_number = type_reg_form.cleaned_data.get('reg_number')
                        if(type):
                            OrganisationRegistration.objects.create(organisation = organisation,type = type,reg_number = reg_number)
            except IntegrityError as e:
                print(e.args[0])
                messages.error(self.request, 'There was an error updating this organisation.')
                return redirect(reverse('crm:update',kwargs={'pk':self.object.pk}))
        return HttpResponseRedirect(self.get_success_url())


class IndexView(TemplateView):
    template_name = 'crm/index.html'
