import django_tables2 as tables
from django_tables2 import A
from django.utils.safestring import mark_safe
from backend.models import Opportunity, Organisation


class OrganisationTable(tables.Table):
    aims_and_activities = tables.Column()
    edit = tables.LinkColumn('crm:update-org', args=[A('pk')], orderable=False, empty_values=(), text='Edit')

    def render_aims_and_activities(self, value):
        return mark_safe(value)

    class Meta:
        model = Organisation
        attrs = {'class': 'paleblue'}


class OpportunityTable(tables.Table):
    description = tables.Column()
    edit = tables.LinkColumn('crm:update-opp', args=[A('pk')], orderable=False, empty_values=(), text='Edit')
    delete = tables.LinkColumn('crm:delete-opp', args=[A('pk')], orderable=False, empty_values=(), text='Delete')

    def render_description(self, value):
        return mark_safe(value)

    class Meta:
        model = Opportunity
        attrs = {'class': 'paleblue'}
