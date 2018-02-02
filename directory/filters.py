from django import forms
from backend.models import Organisation, OrganisationType, Opportunity
import django_filters

class OrganisationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    types = django_filters.ModelMultipleChoiceFilter(queryset=OrganisationType.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Organisation
        #fields = ['name', 'aims_and_activities', 'postcode', 'address', 'types']
        fields = ['name', 'types']


class OpportunityFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Opportunity
        fields = ['name','description','start_date','end_date']
