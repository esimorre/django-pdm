#-*- coding: utf8 -*-
from django.contrib import admin
from models import *

class EntityAdmin(admin.ModelAdmin):
    list_display = ('reference', 'orga', 'creator')
    date_hierarchy = 'created'
    save_as = True
    
    def save_model(self, request, obj, form, change):
        if not change and not self.model.creator:
            self.model.creator = request.user
        super(EntityAdmin, self).save_model(request, obj, form, change)


class ConfAdmin(admin.ModelAdmin):
    list_display = ('reference', 'type')
    list_filter = ('type',)
admin.site.register(Conf, ConfAdmin)

class LinkAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'is_last', 'index', 'created', 'modified')
    list_filter = ('is_last',)
    date_hierarchy = 'created'
    readonly_fields = ('conf',)

class LinkInlineAdmin(admin.TabularInline):
    list_display = ('parent', 'child', 'index')
    # model = Link

class EntityWithConfAdmin(EntityAdmin):
    change_form_template = "admin/pdm/entity_conf/change_form.html"
    
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({'test':'test ok'})
        return super(EntityWithConfAdmin, self).render_change_form(request, context, add, change, form_url, obj)
        