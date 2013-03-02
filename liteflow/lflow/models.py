from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.template.defaultfilters import linebreaks

class Base(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    
    def get_absolute_url(self):
        return "/admin/lflow/%s/%s/" % (self._meta.object_name.lower(), self.pk)
    
    def desc_br(self):
        return linebreaks(self.description)
    desc_br.allow_tags = True
    desc_br.short_description = u"Description"
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        abstract=True


class Processus(Base):
    def get_init_task(self):
        if self.task_set.filter(type=u"start").count() < 1:
            raise Exception("The processus %s has not start task" % self.name)
        return self.task_set.get(type=u"start")
    
    class Meta:
        verbose_name = u"Process"
        verbose_name_plural = u"Processes"

TASK_TYPES = (
(u'start', u'start'),
(u'end', u'end'),
(u'interactive', u'interactive'),
(u'auto', u'auto'),
)
class Task(Base):
    processus = models.ForeignKey(Processus)
    group = models.ForeignKey(Group, null=True, blank=True, related_name='tasks', help_text=u'if not set, only for superusers')
    type = models.CharField(max_length=50, choices=TASK_TYPES)
    
    def visible_actions(self):
        actions = []
        names = []
        for a in self.actions.all():
            av = a.button_label()
            if not av in names:
                actions.append(a)
                names.append(av)
        if not names and self.type in (u'start', u'interactive'):
            raise Exception("The interactive task %s has no visible action" % self.name)
        return actions
    
    def __unicode__(self):
        return "%s:%s" % (self.processus, self.name)
       

class Action(Base):
    label = models.CharField(max_length=50, help_text=u"label of the action button", null=True, blank=True)
    task = models.ForeignKey(Task, related_name='actions')
    target = models.ForeignKey(Task, null=True, blank=True, related_name='input_actions')
    condition = models.CharField(max_length=100, null=True, blank=True,
        help_text=u"ie. getProp('state') == u'Valid'")
    code = models.TextField(null=True, blank=True)
    
    def button_name(self):
        w1 = self.name
        if w1.lower() == "save": return "_save"
        return "_" + w1.lower()
    
    def button_label(self):
        return self.label.split(":")[0]
    
    def is_enabled(self, ob):
        getProp = ob.getProp
        try:
            if self.condition:
                cond = eval(self.condition)
                return cond
        except Exception, v:
            print v
            setProp("ERREUR", v[:99])
        return True
    
    def exec_code(self, ob, f_log, request):
        print self.description
        getProp = ob.getProp
        setProp = ob.setProp
        forward = True
        try:
            src = "\n".join(self.code.splitlines())
            exec(src)
        except Exception, v:
            print v
            forward = False
            setProp("ERREUR", v[:99])
            f_log(request, ob, "action %s erreur:%s" %(self.name, v))
            f_log(request, ob, "action %s forward:%s" %(self.name, forward))
        return forward


class Props(models.Model):
    props = models.CharField(max_length=255, default="{}")
    
    prop_saved = []
    
    def setProp(self, name, value, backup=None):
        dic = eval(unicode(self.props))
        p = dic[name]
        if backup: dic[backup] = dic[name]
        dic[name] = value
        self.props = unicode(dic)
        self.save()
    
    def restoreProp(self, name, name_prev):
        self.setProp(name, self.getProp(name_prev))
    
    def getProp(self, name, default=None):
        dic = eval(unicode(self.props))
        if default:
            if not dic.has_key(name):
                self.setProp(name, default)
                return default
        return dic[name]
    
    class Meta:
        abstract=True

class AbstractComponent(models.Model):
    task = models.ForeignKey(Task, null=True, blank=True, editable=False)
    worker = models.ForeignKey(User, null=True, blank=True, editable=False,
        related_name="%(class)s_components")
    
    def __unicode__(self):
        name = "-"
        if self.task: name = self.task.name
        return "%s:%d" % (name, self.pk)
    
    def task_description(self):
        d = self.task.description
        for k, v in self.link_map.iteritems():
            d = d.replace(k, v)
        return d
    
    def visible_actions(self):
        actions = []
        for a in self.task.visible_actions():
            if a.is_enabled(self): actions.append(a)
        return actions
    
    def action(self, request, f_log):
        if request.POST.has_key("_start_process"):
            self.save_start_process(request.user)
            f_log(request, self, "init process %s" % self.start_processus)
            return
        
        for a in self.task.actions.all():
            print "action a", a.button_name()
            if request.POST.has_key(a.button_name()):
                print 'post'
                if a.exec_code(self, f_log, request):
                    if a.target:
                        self.task = a.target
                        print "current task set to:", self.task
                        self.save()
                        f_log(request, self, "task %s" % self.task.name)
    
    def save_start_processus(self, user, component_type=None):
        self.worker = user
        processus = self.start_processus
        if Processus.objects.filter(name=processus).count() < 1:
            #raise Exception(u"The processus [%s] does not exist." % self.start_processus)
            processus = settings.LITEFLOW_DATA['default_processus']
            if Processus.objects.filter(name=processus).count() < 1:
                raise Exception(u"The processus [%s] does not exist." % self.start_processus)
        self.task = Processus.objects.get(name=processus).get_init_task()
        self.save()
    
    def wait_clones(self, nb=100):
        # parallel pathes junction.
        # return True when the source and nb clones enter the task
        nbclones = self.clones.count()
        nbclones_here = self.clones.filter(task=self.task)
        if nbclones == nb or nbclones_here == nbclones:
            return True
        return False
    
    class Meta:
        abstract = True
        permissions = (
            ("can_start_processus", "Can start a processus"),
            ("can_work_processus", "Can work on a processus"),
        )

class AbstractClone(AbstractComponent):
    # usage: implement this abstract model and add à foreignKey named "source"
    # and a related_name named "clones".
    # for parallel pathes
    def get_source(self):
        # quite useless: use source instead
        return self.source
    
    def wait_clones(self, nb=100):
        # parallel pathes junction.
        # clones are always waiting
        return False
    
    class Meta:
        abstract = True


class Component(AbstractComponent, Base, Props):
    type = models.CharField(max_length=50, editable=False)
    
    link_map = {}
    
    def task_description(self):
        d = super(Component, self).task_description()
        for k, v in self.link_map.iteritems():
            d = d.replace(k, v)
        return d
    
    def save_start_processus(self, user, component_type=None):
        self.type = component_type
        super(Component, self).save_start_processus(user, component_type)
    
    def list_examples(self):
        return Component.objects.filter(type=self.type, description__contains="#Example")
