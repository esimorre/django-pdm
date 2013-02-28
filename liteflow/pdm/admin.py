#-*- coding: utf8 -*-
from django.contrib import admin
from models import *

class EntityAdmin(admin.ModelAdmin):
    list_display = ('reference', 'orga')
    date_hierarchy = 'created'


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

