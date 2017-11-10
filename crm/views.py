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
import mptt

from django_tables2 import SingleTableView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from backend.models import Organisation, OrganisationRegistration, Opportunity, Activity, Skill
from crm.filters import OrganisationFilter
from crm.forms import OrganisationRegistrationForm
from crm.tables import OpportunityTable, OrganisationTable

def get_org_opps(request):
    org_id = request.GET.get('org_id')
    org = Organisation.objects.get(id=org_id)
    opps = Opportunity.objects.filter(organisation=org).values('name','description')
    return HttpResponse(json.dumps(list(opps)))
    # data = serializers.serialize('json',opps)
    #return JsonResponse(opps, safe=False)


def category_belonging_dict(belongingObject, ManyRelatedManagerName):
    """Create a dictionary of MPTT category belonging
    Given the name of an MPTTModel that defines hierarchical categories
    and an object that has belonging of one or more of those categories,
    return a dictionary of categories the object belongs to
    If the MPTT model is say 'Skill', then the ManyRelatedManagerName
    will by default be 'skills', i.e. it is the name used in defining the
    relationship between the model of the category-belonging object and the
    category model with for eg:
    skills = models.ManyToManyField(Skill)
    In django terminology, skills is of type ManyRelatedManager
    """
    catDict = {}
    cats = getattr(belongingObject,ManyRelatedManagerName)
    mpttCats = mptt.utils.tree_item_iterator(cats.all(), ancestors=False)
    for cat in mpttCats:
         catDict[cat[0].name] = cat[0].name
    return catDict


# Create your views here.

class OpportunityDeleteView(DeleteView):
    model = Opportunity
    template_name = 'crm/opportunity_confirm_delete.html'
    success_url = reverse_lazy('crm:list-opps')

class OpportunityUpdateView(UpdateView):
    fields = ('name','description','start_date','end_date','skills','activitys')
    model = Opportunity
    template_name = 'crm/opportunity_update.html'
    success_url = reverse_lazy('crm:list-opps')

    def get_context_data(self, **kwargs):
        context = super(OpportunityUpdateView, self).get_context_data(**kwargs)
        opportunity = Opportunity.objects.get(pk=self.kwargs['pk'])
        context['profileActivities'] = category_belonging_dict(opportunity, 'activitys')
        context['allActivities'] = Activity.objects.all()
        context['profileSkills'] = category_belonging_dict(opportunity, 'skills')
        context['allSkills'] = Skill.objects.all()
        return context

    def form_valid(self, form):
        organisation = form.save()
        print('foo')
        return HttpResponseRedirect(self.get_success_url())

    #     organisation = form.save(commit=False)
    #     type_reg_formset = self.RegistrationFormset(self.request.POST)
    #     if type_reg_formset.is_valid():
    #         try:
    #             with transaction.atomic():
    #                 OrganisationRegistration.objects.filter(organisation=organisation).delete()
    #                 for type_reg_form in type_reg_formset:
    #                     type = type_reg_form.cleaned_data.get('type')
    #                     reg_number = type_reg_form.cleaned_data.get('reg_number')
    #                     if(type):
    #                         OrganisationRegistration.objects.create(organisation = organisation,type = type,reg_number = reg_number)
    #         except IntegrityError as e:
    #             print(e.args[0])
    #             messages.error(self.request, 'There was an error updating this organisation.')
    #             return redirect(reverse('crm:update',kwargs={'pk':self.object.pk}))
    #     return HttpResponseRedirect(self.get_success_url())

    class Meta:
        labels = {
            'name': 'Opportunity title',
            'activitys': 'Activities'
        }

class OpportunityCreateView(CreateView):
    fields = ('organisation','name','description','start_date','end_date')
    model = Opportunity
    template_name = 'crm/opportunity_create.html'
    success_url = reverse_lazy('crm:list-opps')

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


class OrganisationTable(SingleTableMixin,FilterView):
    model = Organisation
    table_class = OrganisationTable
    template_name = 'crm/organisation_table.html'
    table_pagination = {
        'per_page': 10
    }
    filterset_class = OrganisationFilter

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
