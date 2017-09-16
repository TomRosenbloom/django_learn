from django import forms
from backend.models import Organisation, OrganisationType
import django_filters

class OrganisationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    types = django_filters.ModelMultipleChoiceFilter(queryset=OrganisationType.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Organisation
        fields = ['name', 'aims_and_activities', 'postcode', 'address', 'types']
