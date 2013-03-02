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


class LinkAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'is_last', 'index', 'created', 'modified')
    list_filter = ('is_last',)
    date_hierarchy = 'created'

class LinkInlineAdmin(admin.TabularInline):
    list_display = ('child', 'index', 'created', 'modified', 'is_last')
    readonly_fields =('created', 'modified', 'is_last')
    extra = 1

class EntityWithConfAdmin(EntityAdmin):
    change_form_template = "admin/pdm/entity_conf/change_form.html"
    
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context['confs'] = []
        #for cm in self.model.conf_models: context['confs'].append(cm._meta.verbose_name)
        context.update({'test':'test ok'})
        return super(EntityWithConfAdmin, self).render_change_form(request, context, add, change, form_url, obj)
        