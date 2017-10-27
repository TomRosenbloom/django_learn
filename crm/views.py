from django.shortcuts import render, redirect
from django.views.generic import (View, TemplateView, FormView,
                                ListView, DetailView, CreateView,
                                UpdateView, DeleteView)
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import formset_factory
from backend.models import Organisation, OrganisationRegistration
from crm.forms import OrganisationRegistrationForm


# Create your views here.

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
            for type_reg_form in type_reg_formset:
                type = type_reg_form.cleaned_data.get('type')
                reg_number = type_reg_form.cleaned_data.get('reg_number')
                print(type)
                print(reg_number)
                OrganisationRegistration.objects.create(
                    organisation = organisation,
                    type = type,
                    reg_number = reg_number
                    )
        return HttpResponseRedirect(self.get_success_url())


class IndexView(TemplateView):
    template_name = 'crm/index.html'
