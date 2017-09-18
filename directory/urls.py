from django.conf.urls import url
from . import views

from django_filters.views import FilterView
from backend.models import Organisation
from directory.filters import OrganisationFilter

app_name = 'directory'

urlpatterns = [
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^list/$',views.OrganisationListView.as_view(),name='list'),
    url(r'^list/(?P<pk>[-\w+])$',views.OrganisationDetailView.as_view()),
    url(r'^search/$',views.search, name='search'),
    # filter CBV version
    url(r'^filter/$',FilterView.as_view(filterset_class=OrganisationFilter,
        template_name='directory/organisation_filter.html'),name='filter'),
    url(r'^export/csv/$', views.export_organisations_csv, name='export_organisations_csv'),
]
