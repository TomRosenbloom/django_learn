from django.conf.urls import url
from . import views

from django_filters.views import FilterView
from backend.models import Organisation
from directory.filters import OrganisationFilter

app_name = 'directory'

urlpatterns = [
    url(r'^$',views.IndexView.as_view(),name='index'),

    # url(r'^list/$',views.OrganisationListView.as_view(),name='list'),
    # url(r'^list/(?P<pk>\d+)$',views.OrganisationDetailView.as_view()),

    url(r'^organisations/$',views.OrganisationFilterView.as_view(), name='orgs'),
    url(r'^organisation/detail/(?P<pk>\d+)$',views.OrganisationDetailView.as_view(),name='org'),
    url(r'^organisation/detail/(?P<pk>\d+)/(?P<opp_id>\d+)$',views.OrganisationDetailView.as_view(),name='org'),

    url(r'^opportunities/$',views.OpportunityFilterView.as_view(), name='opps'),
    url(r'^opportunity/detail/(?P<pk>\d+)$',views.OpportunityDetailView.as_view(),name='opportunity'),

    url(r'^export/csv/$', views.export_organisations_csv, name='export_organisations_csv'),

]
