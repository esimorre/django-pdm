#-*- coding: utf8 -*-
from django.contrib import admin
from ..pdm.admin import *
from models import *

class DocumentationInlineAdmin(LinkInlineAdmin):
    model = ProductDocumentation

class CompositionInlineAdmin(LinkInlineAdmin):
    model = Composition
    fk_name = 'parent'

class ProductAdmin(EntityWithConfAdmin):
    actions = [action_new_version,]
    inlines = [DocumentationInlineAdmin, CompositionInlineAdmin]
admin.site.register(Product, ProductAdmin)

admin.site.register(Document, VersionedEntityAdmin)


admin.site.register(Composition, LinkAdmin)
admin.site.register(Content, LinkAdmin)
admin.site.register(ProductDocumentation, LinkAdmin)


from ..lflow.admin import ComponentProcessusAdmin
class PartAdmin(ComponentProcessusAdmin):
    pass
admin.site.register(Part, PartAdmin)

class WorkItemAdmin(ComponentProcessusAdmin):
    pass
admin.site.register(SimpleWorkItem, WorkItemAdmin)

class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')
admin.site.register(Car, CarAdmin)
