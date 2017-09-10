from django.conf.urls import url
from . import views

app_name = 'org_reg'

urlpatterns = [
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^signup/$',views.OrgSignUpView.as_view(),name='signup'),
    url(r'^profile/$',views.ProfileView.as_view(),name='profile'),
    url(r'^login/$',views.OrgLoginView.as_view(),name='login'),
    url(r'^logout/$',views.org_logout,name='logout'),
]
