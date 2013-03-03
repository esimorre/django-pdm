from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType

from ..rights.models import Organization

class Entity(models.Model):
    reference = models.CharField(max_length=30, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    orga = models.ForeignKey(Organization, null=True, blank=True)
    creator = models.ForeignKey(User, null=True, blank=True, editable=False, related_name="%(class)s_entities")
    
    state = models.CharField(max_length=30, default='created')
    confs = []
    
    # model is a Link-based model
    @classmethod
    def register_conf(cls, model):
        if not model in cls.confs: cls.confs.append(model)
    
    def check_out(self):
        pass
        # return a new entity
    
    def __unicode__(self):
        return self.reference
    
    class Meta:
        abstract = True

class VersionedEntity(Entity):
    origin = models.ForeignKey('self', null=True, blank=True)
    
    def new_version(self):
        from versioning import get_next_reference
        pk_origin = self.pk
        self.pk = None
        self.reference = get_next_reference(self.reference)
        self.save()
        self.origin = self._default_manager.get(pk=pk_origin)
        self.save()
        self._copy_confs(self.origin)
    
    def _copy_confs(self, obj_src):
        for conf in self.confs:
            for link in conf.objects.filter(parent=link.parent):
                link.copy(parent=self)
            for link in conf.objects.filter(child=link.child):
                link.copy(child=self)
    
    class Meta:
        abstract = True


class Link(models.Model):
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
    
    def copy(self, parent=None, child=None):
        print "link copy", parent, child
        self.pk = None
        if parent: self.parent = parent
        if child: self.child = child
    
    def save(self, write_nolast=False, *largs, **kwargs):
        if not self.pk:
            # creation
            for l in self._default_manager.filter(parent=self.parent, child=self.child, is_last=True):
                l.is_last = False
                l.save(write_nolast=True)
        else:
            if not self.is_last and not write_nolast:
                raise Exception("a non last link cannot be modified")
        super(Link, self).save(*largs, **kwargs)
    
    def __unicode__(self):
        return "%s -> %s" % (self.get_parent(), self.get_child())
        
    class Meta:
        abstract = True

