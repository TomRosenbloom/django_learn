from django.conf.urls import url
from . import views

app_name = 'org_reg'

urlpatterns = [
    url(r'^$',views.IndexView.as_view(),name='index'),
    #url(r'^$',views.index,name='index'),
    url(r'^signup/$',views.OrgSignUpView.as_view(),name='signup'),
    url(r'^profile/$',views.ProfileView.as_view(),name='profile'),
    url(r'^login/$',views.OrgLogin.as_view(),name='login'),
    url(r'^logout/$',views.OrgLogout.as_view(),name='logout'),
    url(r'^detail/(?P<pk>[-\w+])$',views.OrganisationDetailView.as_view(),name='detail'),
    url(r'^create/$',views.OrganisationCreateView.as_view(),name='create'),
    url(r'^update/(?P<pk>[-\w+])$',views.OrganisationUpdateView.as_view(),name='update'),
    url(r'^delete/(?P<pk>[-\w+])$',views.OrganisationDeleteView.as_view(),name='delete'),
    url(r'^select/$',views.OrganisationSelect.as_view(),name='select')    
]
