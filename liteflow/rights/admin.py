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


class RightModelAdmin(admin.ModelAdmin):
    right_fields = ('state', 'organization')
    
    realy_change_perm_needed = False
    
    def queryset(self, request):
        qs = super(RightModelAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        if 'organization' in self.right_fields:
            list_orgas = Right.objects.visible_organizations_names(request.user)
            if not u'Any' in list_orgas:
                qs = qs.filter(organization__in=list_orgas)
        if 'state' in self.right_fields:
            states = Right.objects.visible_states(request.user, self.model)
            if not u'Any' in states:
                qs = qs.filter(state__in=states)
        return qs
    
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'organization':
            if not request.user.is_superuser:
                list_orgas = Right.objects.visible_organizations_names(request.user)
                if not u'Any' in list_orgas:
                    kwargs['queryset'] = Organization.objects.filter(name__in=list_orgas)
        ff = super(RightModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        return ff
    
    def get_readonly_fields(self, request, obj=None):
        print "get_readonly_fields", obj
        if not obj and 'state' in self.right_fields:
            l = Right.objects.get_rights(request.user, self.model, u'Create')
            print l[0].state
            if len(l) == 1 and l[0].state != u'Any':
                if not 'state' in self.readonly_fields:
                    self.readonly_fields = list(self.readonly_fields)
                    self.readonly_fields.append('state')
        fields = [f.name for f in self.model._meta.fields]
        return self.readonly_fields

    def get_model_perms(self, request):
        """
        Returns a dict of all perms for this model. This dict has the keys
        ``add``, ``change``, and ``delete`` mapping to the True/False for each
        of those actions.
        """
        return {
            'add': self.has_add_permission(request),
            'change': self.has_change_permission(request),
            'read': self.has_read_permission(request),
            'delete': self.has_delete_permission(request),
        }
    
    def has_add_permission(self, request):

        return Right.objects.get_rights(request.user, self.model, u'Create').count() > 0
        
    def has_read_permission(self, request):
        return len( Right.objects.visible_states(request.user, self.model) ) > 0
    
    def has_update_permission(self, request, obj=None):
        qs = Right.objects.get_rights(request.user, self.model, u'Update')
        if obj:
            qs = qs.filter(state=obj.state)
        return  qs.count() > 0
    
    def has_change_permission(self, request, obj=None):
        b = super(RightModelAdmin, self).has_change_permission(request, obj)
        if self.realy_change_perm_needed:
            return b or self.has_update_permission(request, obj)
        if self.has_update_permission(request):
            return True
        if not b and self.has_read_permission(request):
            return True
        return b
        
    def save_model(self, request, obj, form, change):
        if not change and 'state' in self.right_fields:
            l = Right.objects.get_rights(request.user, self.model, u'Create')
            if len(l) == 1 and l[0].state != u'Any':
                obj.state = l[0].state
        return super(RightModelAdmin, self).save_model(request, obj, form, change)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        self.realy_change_perm_needed = True
        context['has_read_permission'] = self.has_read_permission(request)
        f = super(RightModelAdmin, self).render_change_form(request, context, add, change, form_url, obj)
        self.realy_change_perm_needed = False
        return f
    def changelist_view(self, request, extra_context=None):
        if not extra_context: extra_context = {}
        extra_context['has_change_permission'] = self.has_change_permission(request)
        extra_context['has_read_permission'] = self.has_read_permission(request)
        return super(RightModelAdmin, self).changelist_view(request, extra_context)

def action_resetcache(modeladmin, request, queryset):
    modeladmin.model.objects.reset_cache()
action_resetcache.short_description = "Reset rights cache"

class RightAdmin(RightModelAdmin):
    actions = [action_resetcache]
    right_fields = ('organization',)
    list_display = ('organization', 'content_type', 'group', 'operation', 'state')
    list_filter = ('organization', 'operation', 'content_type', 'group')
    save_as = True
admin.site.register(Right, RightAdmin)


from django.contrib.auth.models import Permission
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'content_type', 'codename')
    list_filter = ('codename', 'content_type')
admin.site.register(Permission, PermissionAdmin)
