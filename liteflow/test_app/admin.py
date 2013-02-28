#-*- coding: utf8 -*-
from django.contrib import admin
from ..pdm.admin import LinkInlineAdmin, ConfAdmin, LinkAdmin
from models import *

admin.site.register(Product)
admin.site.register(Document)


admin.site.register(Composition, LinkAdmin)
admin.site.register(Content, LinkAdmin)
admin.site.register(ProductDocumentation, LinkAdmin)


class ContentAdmin(LinkInlineAdmin):
    model = Content
class ConfContentAdmin(ConfAdmin):
    inlines = [ContentAdmin,]
admin.site.register(ConfContent, ConfContentAdmin)


class CompositionAdmin(LinkInlineAdmin):
    model = Composition
class ConfCompositionAdmin(ConfAdmin):
    inlines = [CompositionAdmin,]
admin.site.register(ConfComposition, ConfCompositionAdmin)


class ProductDocumentationAdmin(LinkInlineAdmin):
    model = ProductDocumentation
class ConfProductDocumentationAdmin(ConfAdmin):
    inlines = [ProductDocumentationAdmin,]
admin.site.register(ConfProductDocumentation, ConfProductDocumentationAdmin)

from ..lflow.admin import ComponentProcessusAdmin
class PartInProcessusAdmin(ComponentProcessusAdmin):
    pass
admin.site.register(PartInProcessus, PartInProcessusAdmin)

class WorkItemAdmin(ComponentProcessusAdmin):
    component_type = "Work item"
admin.site.register(SimpleWorkItem, WorkItemAdmin)