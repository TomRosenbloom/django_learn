from django.contrib import admin

from .models import UserProfile, Volunteer, Org_user





# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Volunteer)
admin.site.register(Org_user)
