from django.db import models
from django.contrib.auth.models import User

from ..pdm.models import Entity, Link, VersionedEntity


class Product(VersionedEntity):
    image = models.FileField(upload_to="documents", null=True, blank=True)
    type = models.CharField(max_length=20)
    

class Document(VersionedEntity):
    file = models.FileField(upload_to="documents", null=True, blank=True)
    author = models.CharField(max_length=50)



class Composition(Link):
    parent = models.ForeignKey(Product, related_name="parent_links")
    child = models.ForeignKey(Product, related_name="child_links")
    class Meta:
        verbose_name = "Composition link"

Product.register_conf(Composition)

class ProductDocumentation(Link):
    parent = models.ForeignKey(Product)
    child = models.ForeignKey(Document)
    class Meta:
        verbose_name = "Product documentation link"

Product.register_conf(ProductDocumentation)
Document.register_conf(ProductDocumentation)


class Content(Composition):
    class Meta:
        proxy = True
        verbose_name = "Content link"

Product.register_conf(Content)

from ..lflow.models import Component, AbstractComponent

class Part(Entity, AbstractComponent):
    start_processus = 'Product process'
    info = models.CharField(max_length=50)


class SimpleWorkItem(Component):
    start_processus = 'Product process'
    
    class Meta:
        proxy = True

STATE_CHOICES = (
(u'created', u'created'),
(u'valid', u'valid'),
(u'released', u'released'),
(u'obsolete', u'obsolete'),
)
class Car(models.Model):
    state = models.CharField(max_length=30, null=True, blank=True, choices=STATE_CHOICES)
    name = models.CharField(max_length=20)
    class Meta:
        permissions = (
            ("visible_admin", "Visible in admin"),
        )
