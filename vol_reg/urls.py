from django.conf.urls import url
from . import views

app_name = 'vol_reg'

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^signup/$',views.signup,name='signup'), #working from this url https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
    url(r'^register/$',views.register,name='register'),
    url(r'^registration_form/$', views.registration_form, name="registration_form"),
]
