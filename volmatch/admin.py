from django.contrib import admin

from address.models import AddressField
from address.forms import AddressWidget


from volmatch.models import UserProfile, Volunteer





# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Volunteer)
