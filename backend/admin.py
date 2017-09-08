from django.contrib import admin

from address.models import AddressField
from address.forms import AddressWidget

from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin

from backend.models import Funder, Project, Organisation, Person, Role, Person_org_role, Profile, Skill, Activity, OrganisationType, OrganisationRegistration



class OrganisationRegistrationInLine(admin.TabularInline):
    model = OrganisationRegistration
    extra = 1


class OrganisationAdmin(admin.ModelAdmin):
    formfield_overrides = {
        AddressField: {'widget': AddressWidget(attrs={'style': 'width: 300px;'})}
    }
    inlines = (OrganisationRegistrationInLine,)


# Register your models here.
admin.site.register(Funder)
admin.site.register(Project)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(OrganisationType)
admin.site.register(OrganisationRegistration)
admin.site.register(Person)
admin.site.register(Role)
admin.site.register(Person_org_role)
admin.site.register(Profile)
admin.site.register(Skill, MPTTModelAdmin)

admin.site.register(
    Activity,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    ),
)
