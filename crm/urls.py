from django.conf.urls import url
from . import views

app_name = 'crm'

urlpatterns = [
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^organisations/list/$',views.OrganisationTable.as_view(),name='list-orgs'),
    url(r'^opportunities/list/$',views.OpportunityTable.as_view(),name='list-opps'),
    url(r'^opportunity/(?P<pk>\d+)$',views.OpportunityUpdateView.as_view(),name='update-opp'),
    url(r'^opportunity/delete/(?P<pk>\d+)$',views.OpportunityDeleteView.as_view(),name='delete-opp'),
    url(r'^opportunity/create/$',views.OpportunityCreateView.as_view(),name='create-opp'),

    url(r'^ajax/org_opps/$',views.get_org_opps, name='ajax_org_opps'),

    url(r'^organisation/update/(?P<pk>\d+)$',views.OrganisationUpdateView.as_view(),name='update-org'), # need 'organisation' in url
]
