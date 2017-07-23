from django.conf.urls import url
from . import views

app_name = 'vol_reg'

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^register/$',views.register,name='register'),
    url(r'^registration_form/$', views.registration_form, name="registration_form"),
]
