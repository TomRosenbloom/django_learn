from django.conf.urls import url
from . import views

app_name = 'org_reg'

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^signup/$',views.signup,name='signup'),
    url(r'^profile/$',views.profile,name='profile'),
    url(r'^login/$',views.org_login,name='login'),
]
