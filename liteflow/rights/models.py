from django.db import models
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType


class Organization(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    
    def __unicode__(self):
        return self.name

OPERATION_CHOICES = (
(u'Any', u'Any'),
(u'Creation', u'Creation'),
(u'Manage', u'Manage'),
(u'Oper1', u'Oper1'),
)
class Right(models.Model):
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    group = models.ForeignKey(Group, null=True, blank=True)
    organization = models.ForeignKey(Organization, null=True, blank=True)
    operation = models.CharField(max_length=50, choices=OPERATION_CHOICES)
