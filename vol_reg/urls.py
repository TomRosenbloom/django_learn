from django.conf.urls import url
from . import views

app_name = 'vol_reg'

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^signup/$',views.signup,name='signup'),
    url(r'^profile/$',views.profile,name='profile'),
    url(r'^login/$',views.VolLogin.as_view(),name='login'),
    url(r'^logout/$',views.VolLogout.as_view(),name='logout'),
    url(r'^not_authorised/$',views.NotAuthorised.as_view(),name='not_authorised'),

]
