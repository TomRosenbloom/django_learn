from django.conf.urls import url
from . import views

app_name = 'org_reg'

urlpatterns = [
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^signup/$',views.OrgSignUpView.as_view(),name='signup'),
    url(r'^profile/$',views.ProfileView.as_view(),name='profile'),
    url(r'^login/$',views.OrgLogin.as_view(),name='login'),
    url(r'^logout/$',views.OrgLogout.as_view(),name='logout'),
    url(r'^detail/(?P<pk>\d+)$',views.OrganisationDetailView.as_view(),name='detail'),
    url(r'^create/$',views.OrganisationCreateView.as_view(),name='create'),
    url(r'^update/(?P<pk>\d+)$',views.OrganisationUpdateView.as_view(),name='update'),
    url(r'^delete/(?P<pk>\d+)$',views.OrganisationDeleteView.as_view(),name='delete'),
    url(r'^select/$',views.OrganisationSelect.as_view(),name='select'),
    url(r'^opportunity/org_id/(?P<organisation>\d+)$',views.OpportunityCreateView.as_view(),name='opportunity'),
    url(r'^opportunity/(?P<pk>\d+)$',views.OpportunityUpdateView.as_view(),name='update_opp'),
    url(r'^opportunity/delete/(?P<pk>\d+)$',views.OpportunityDeleteView.as_view(),name='delete_opp'),
    url(r'^leave/(?P<organisation>\d+)$',views.OrganisationLeave.as_view(),name='leave'),
    # this is for an org user 'leaving' an org - should this be here or in user_types app?
]
