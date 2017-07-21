"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from backend import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from backend import views
#from vol_reg import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^formpage/',views.form_view,name="form_name"),

    url(r'^orgform', views.org_addr_form, name='foo'),

    url(r'^other',views.other,name='other'),

    url(r'^volunteer/', include('vol_reg.urls')),

]
