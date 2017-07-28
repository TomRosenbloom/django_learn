from django.conf.urls import url
from . import views

app_name = 'vol_reg'

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^signup/$',views.signup,name='signup'),
    url(r'^welcome/$',views.welcome,name='welcome'),
    url(r'^profile/$',views.profile,name='profile'),
    #url(r'^profile_form/$', views.profile_form, name="profile_form"),
]
