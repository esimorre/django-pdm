#-*- coding: utf8 -*-
from django.contrib import admin
from models import *


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Organization, OrganizationAdmin)

class RightAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'organization', 'group', 'operation')
    list_filter = ('organization', 'group', 'operation', 'content_type')
admin.site.register(Right, RightAdmin)


from django.contrib.auth.models import Permission
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'content_type', 'codename')
    list_filter = ('codename', 'content_type')
admin.site.register(Permission, PermissionAdmin)
