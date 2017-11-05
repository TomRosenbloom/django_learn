from django import forms
from backend.models import Organisation, OrganisationType
import django_filters
from django_filters import filters

filters.LOOKUP_TYPES = [
    ('', '---------'),
    ('istartswith', 'Starts with'),
    ('icontains', 'Contains'),
]
# https://docs.djangoproject.com/en/1.11/ref/models/querysets/#field-lookups
# ...lots of useful options: range, date, year, month
# ...but 'search' deprecated since 1.10

class OrganisationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr=['icontains','istartswith'])
    telephone = django_filters.CharFilter(lookup_expr=['icontains','istartswith'])
    types = django_filters.ModelChoiceFilter(queryset=OrganisationType.objects.all(), empty_label='Organisation type')

    class Meta:
        model = Organisation
        #fields = ['name', 'aims_and_activities', 'postcode', 'address', 'types']
        fields = ['name', 'types', 'telephone', 'postcode']
