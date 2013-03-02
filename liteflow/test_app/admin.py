#-*- coding: utf8 -*-
from django.contrib import admin
from ..pdm.admin import *
from models import *

admin.site.register(Product, EntityWithConfAdmin)

admin.site.register(Document, EntityAdmin)


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
class PartAdmin(ComponentProcessusAdmin):
    pass
admin.site.register(Part, PartAdmin)

class WorkItemAdmin(ComponentProcessusAdmin):
    pass
admin.site.register(SimpleWorkItem, WorkItemAdmin)