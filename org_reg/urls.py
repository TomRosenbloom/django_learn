from django.conf.urls import url
from . import views

app_name = 'org_reg'

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^signup/$',views.signup,name='signup'),
    url(r'^profile/$',views.ProfileView.as_view(),name='profile'),
    url(r'^login/$',views.org_login,name='login'),
    url(r'^foo/$',views.Foo.as_view())
]
