from django.contrib import admin

from address.models import AddressField
from address.forms import AddressWidget

from backend.models import Funder, Project, Organisation


class OrganisationAdmin(admin.ModelAdmin):
    formfield_overrides = {
        AddressField: {'widget': AddressWidget(attrs={'style': 'width: 300px;'})}
    }

# Register your models here.
admin.site.register(Funder)
admin.site.register(Project)
admin.site.register(Organisation, OrganisationAdmin)
