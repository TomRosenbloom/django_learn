from django.contrib import admin

from address.models import AddressField
from address.forms import AddressWidget

from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin

from volmatch.models import UserProfile, Skill, Activity, Volunteer





# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Volunteer)
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
