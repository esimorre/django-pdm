from django.db import models
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType


class Organization(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    
    def __unicode__(self):
        return self.name

OPERATION_CHOICES = (
(u'Any', u'Any'),
(u'Read', u'Read'),
(u'Update', u'Update'),
(u'Create', u'Create'),
(u'Manage', u'Manage'),
(u'Oper1', u'Oper1'),
)

STATE_CHOICES = (
(u'Any', u'Any'),
(u'created', u'created'),
(u'valid', u'valid'),
(u'released', u'released'),
(u'obsolete', u'obsolete'),
)

class RightManager(models.Manager):
    # cache[username] = {'orgas': list_orga_names, }
    cache = {}
    def visible_organizations(self, user):
        return self.get_rights(user).values_list('organization')
    
    def visible_organizations_names(self, user):
        if not self.cache.has_key(user.username):
            self.cache[user.username] = {}
        if not self.cache[user.username].has_key('orgas'):
            self.cache[user.username]['orgas'] = [o.name for o in self.visible_organizations(user)]
        return self.cache[user.username]['orgas']
    
    def visible_states_names(self, user, model):
        model_name = model._meta.object_name
        if not self.cache.has_key(user.username):
            self.cache[user.username] = {}
        if not self.cache[user.username].has_key('states'):
            self.cache[user.username]['states'] = {}
        if not self.cache[user.username]['states'].has_key(model_name):
            self.cache[user.username]['states'][model_name] = [r.state for r in self.get_rights(user, model)]
        return self.cache[user.username]['states'][model_name]
    
    def reset_cache(self, user=None):
        if not user: self.cache = {}
        else:
            self.cache[user.username] = {}
    
    def get_rights(self, user, model=None):
        qs = self.filter(group__in=user.groups)
        if model:
            return qs.filter(content_type=ContentType.objects.get_for_model(model))

class Right(models.Model):
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    group = models.ForeignKey(Group, null=True, blank=True)
    organization = models.ForeignKey(Organization, null=True, blank=True)
    operation = models.CharField(max_length=50, choices=OPERATION_CHOICES)
    state = models.CharField(max_length=30, null=True, blank=True, choices=STATE_CHOICES)
    
    objects = RightManager()
    