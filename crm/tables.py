import django_tables2 as tables
from django_tables2 import A
from django.utils.safestring import mark_safe
from backend.models import Opportunity

class OpportunityTable(tables.Table):
    description = tables.Column()
    edit = tables.LinkColumn('crm:update-opp', args=[A('pk')], orderable=False, empty_values=(), text='Edit')
    delete = tables.LinkColumn('crm:delete-opp', args=[A('pk')], orderable=False, empty_values=(), text='Delete')

    def render_description(self, value):
        return mark_safe(value)

    class Meta:
        model = Opportunity
        attrs = {'class': 'paleblue'}
