from django.contrib import admin
from .models import (
    ProcessDefinition,
    RegisteredTask,
    ProcessTask,
    Process,
    Task
)

class ProcessTasksInline(admin.TabularInline):
    model = ProcessTask

class ProcessDefinitionAdmin(admin.ModelAdmin):
    inlines = [ProcessTasksInline,]

class TaskInline(admin.TabularInline):
    model = Task

class ProcessAdmin(admin.ModelAdmin):
    inlines = [TaskInline,]

admin.site.register(ProcessDefinition, ProcessDefinitionAdmin)
admin.site.register(Process, ProcessAdmin)
admin.site.register(RegisteredTask)
admin.site.register(ProcessTask)
admin.site.register(Task)