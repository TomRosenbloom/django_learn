from django.contrib import admin

from address.models import AddressField
from address.forms import AddressWidget

from backend.models import Funder, Project, Organisation, Person, Role, Person_org_role, Profile


class OrganisationAdmin(admin.ModelAdmin):
    formfield_overrides = {
        AddressField: {'widget': AddressWidget(attrs={'style': 'width: 300px;'})}
    }

# Register your models here.
admin.site.register(Funder)
admin.site.register(Project)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Person)
admin.site.register(Role)
admin.site.register(Person_org_role)
admin.site.register(Profile)
