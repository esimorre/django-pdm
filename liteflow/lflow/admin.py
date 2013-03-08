#-*- coding: utf8 -*-
from django.contrib import admin
from models import *

class TaskInlineAdmin(admin.TabularInline):
    model = Task
    extra = 0

class ActionInlineAdmin(admin.StackedInline):
    model = Action
    extra = 0

class ProcessusAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    save_as = True
    inlines = [TaskInlineAdmin, ActionInlineAdmin]
admin.site.register(Processus, ProcessusAdmin)


# disabled
class ActionAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc_br', 'task', 'target')
    list_filter = ('task', 'target')
    prepopulated_fields = {"label":("name",)}
    save_as = True
#admin.site.register(Action, ActionAdmin)

# disabled
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc_br', 'type', 'processus', 'group')
    list_filter = ('processus', 'type', 'group')
    save_as = True
#admin.site.register(Task, TaskAdmin)

class ComponentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'type', 'worker', 'task')
    list_filter = ('type', 'worker', 'task')
    save_as = True
admin.site.register(Component, ComponentAdmin)

class ComponentProcessusAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'worker', 'task')
    list_filter = ('worker', 'task')
    save_on_top = True
    
    change_form_template = "admin/lflow/compproc/change_form.html"
    add_form_template = "admin/lflow/compproc/add_form.html"
    
    def queryset(self, request):
        qs = super(ComponentProcessusAdmin, self).queryset(request)
        if hasattr(self, 'type'):
            qs = qs.filter(type=self.model._meta.object_name)
        if not request.user.is_superuser:
            qs = qs.filter(task__group__in=request.user.groups.all())
        return qs.exclude(task__type='end')
    
    def get_model_perms(self, request):
        perms = super(ComponentProcessusAdmin, self).get_model_perms(request)
        perm = self.opts.app_label + ".can_%s_processus"
        # if Component proxy, select perms on Component
        if self.model._meta.proxy:
            if self.model._meta.proxy_for_model == Component:
                perm = "lflow.can_%s_processus"
        print perm % 'work', request.user, self.model
        perms.update({'work':request.user.has_perms((perm % 'work',)), 'start':request.user.has_perms((perm % 'start',))})
        return perms
    
    def save_model(self, request, obj, form, change):
        #print "change", change
        if not change:
            obj.save_start_processus(request.user, self.model._meta.object_name)
            self.log_change(request, obj, "init processus %s" % obj.start_processus)
        else:
            obj.action(request, self.log_change)