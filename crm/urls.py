from django.conf.urls import url
from . import views

app_name = 'crm'

urlpatterns = [
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^list/$',views.OrganisationListView.as_view(),name='list'),
    url(r'^opportunities/list/$',views.OpportunityTable.as_view(),name='list-opps'),
    url(r'^opportunity/(?P<pk>\d+)$',views.OpportunityUpdateView.as_view(),name='update-opp'),
    url(r'^opportunity/delete/(?P<pk>\d+)$',views.OpportunityDeleteView.as_view(),name='delete-opp'),
    # url(r'^login/$',views.OrgLogin.as_view(),name='login'),
    # url(r'^logout/$',views.OrgLogout.as_view(),name='logout'),
    #url(r'^detail/(?P<pk>\d+)$',views.OrganisationDetailView.as_view(),name='detail'),
    # url(r'^create/$',views.OrganisationCreateView.as_view(),name='create'),
    url(r'^update/(?P<pk>\d+)$',views.OrganisationUpdateView.as_view(),name='update'),
    # url(r'^delete/(?P<pk>\d+)$',views.OrganisationDeleteView.as_view(),name='delete'),
]
