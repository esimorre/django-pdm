#-*- coding: utf8 -*-
from django.contrib import admin
from models import *

# actions
def action_copy(modeladmin, request, queryset):
    pass
action_copy.short_description = "Copy rights (NYI)"

def action_paste(modeladmin, request, queryset):
    pass
action_paste.short_description = "Paste rights (NYI)"


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    actions = [action_copy, action_paste]
    
admin.site.register(Organization, OrganizationAdmin)

class RightAdmin(admin.ModelAdmin):
    list_display = ('organization', 'content_type', 'group', 'operation', 'state')
    list_filter = ('organization', 'operation', 'content_type', 'group')
admin.site.register(Right, RightAdmin)


class RightModelAdmin(admin.ModelAdmin):
    right_fields = ('state', 'organization')
    def queryset(self, request):
        qs = super(RightModelAdmin, self).queryset(request)
        if 'organization' in self.right_fields:
            qs = qs.filter(organization__in=Right.objects.visible_organizations_names(request.user))
        if 'state' in self.right_fields:
            qs = qs.filter(state__in=Right.objects.visible_states(request.user, self.model))
        return qs


from django.contrib.auth.models import Permission
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'content_type', 'codename')
    list_filter = ('codename', 'content_type')
admin.site.register(Permission, PermissionAdmin)
