from django.conf.urls import url
from . import views

app_name = 'directory'

urlpatterns = [
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^list/$',views.OrganisationListView.as_view(),name='list'),
    url(r'^list/(?P<pk>[-\w+])$',views.OrganisationDetailView.as_view()),
    url(r'^search/$',views.search, name='search'),
]
