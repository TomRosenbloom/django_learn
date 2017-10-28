import django_tables2 as tables
from backend.models import Opportunity

class OpportunityTable(tables.Table):
    class Meta:
        model = Opportunity
        attrs = {'class': 'paleblue'}
