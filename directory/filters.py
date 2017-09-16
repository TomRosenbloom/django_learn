from backend.models import Organisation
import django_filters

class OrganisationFilter(django_filters.FilterSet):
    class Meta:
        model = Organisation
        fields = ['name', 'aims_and_activities', 'postcode', 'types']
