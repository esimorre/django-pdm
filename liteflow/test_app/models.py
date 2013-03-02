from django.db import models
from django.contrib.auth.models import User

from ..pdm.models import Entity, Link, Conf, ConfManager

class Product(Entity):
    image = models.FileField(upload_to="documents", null=True, blank=True)
    type = models.CharField(max_length=20)

class Document(Entity):
    file = models.FileField(upload_to="documents", null=True, blank=True)
    author = models.CharField(max_length=50)



class Composition(Link):
    parent = models.ForeignKey(Product, related_name="parent_links")
    child = models.ForeignKey(Product, related_name="child_links")
    class Meta:
        verbose_name = "Composition link"

class ConfComposition(Conf):
    objects = ConfManager()
    class Meta:
        proxy = True
        verbose_name = "Composition configuration"


class ProductDocumentation(Link):
    parent = models.ForeignKey(Product)
    child = models.ForeignKey(Document)
    class Meta:
        verbose_name = "Product documentation link"

class ConfProductDocumentation(Conf):
    objects = ConfManager()
    class Meta:
        proxy = True
        verbose_name = "Product documentation configuration"


class Content(Composition):
    class Meta:
        proxy = True
        verbose_name = "Content link"

class ConfContent(Conf):
    objects = ConfManager()
    class Meta:
        proxy = True
        verbose_name = "Content configuration"

from ..lflow.models import Component, AbstractComponent
class PartInProcessus(Entity, AbstractComponent):
    start_processus = 'Product process'
    info = models.CharField(max_length=50)


class SimpleWorkItem(Component):
    start_processus = 'Product process'
    
    class Meta:
        proxy = True
