from django.conf.urls import url
from . import views

app_name = 'vol_reg_alt'

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^register/$',views.register,name='register'),
    #url(r'^)
]
