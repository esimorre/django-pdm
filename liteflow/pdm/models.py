from django.db import models
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType

from ..rights.models import Organization

class Entity(models.Model):
    reference = models.CharField(max_length=30, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    orga = models.ForeignKey(Organization, null=True, blank=True)
    
    state = models.CharField(max_length=30, default='created')
    
    def get_or_create_conf(self, model):
        pass
    
    def check_out(self):
        pass
        # return a new entity
    
    def next_ref(self):
        pass
        #return next ref
    
    def __unicode__(self):
        return self.reference
    
    class Meta:
        abstract = True

class ConfManager(models.Manager):
    def get_query_set(self):
        return super(ConfManager, self).get_query_set().filter(type=self.model._meta.object_name)
        
class Conf(models.Model):
    type = models.CharField(max_length=50, null=True, blank=True, editable=False)
    reference = models.CharField(max_length=30,  null=True, blank=True, editable=False)
    
    def add_child(self, entity):
        pass
        # todo create link
    
    def save(self, *largs, **kwargs):
        if not self.type:
            self.type = self._meta.object_name
        super(Conf, self).save(*largs, **kwargs)
    
    def __unicode__(self):
        return self.reference
    
class Link(models.Model):
    conf = models.ForeignKey(Conf)
    rev_start = models.IntegerField(null=True, blank=True, editable=False)
    rev_end = models.IntegerField(null=True, blank=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    index = models.IntegerField(null=True, blank=True)
    is_last = models.BooleanField(default=True, editable=False)
   
    def get_parent(self):
        # parent must be a concrete Entity
        return self.parent
    
    def get_child(self):
        # child must be a concrete Entity
        return self.child
     
    def save(self, *largs, **kwargs):
        super(Link, self).save(*largs, **kwargs)
        if not self.conf.reference:
            self.conf.reference = self.get_parent().reference
            self.conf.save()
    
    def __unicode__(self):
        return "%s -> %s" % (self.get_parent(), self.get_child())
        
    class Meta:
        abstract = True

