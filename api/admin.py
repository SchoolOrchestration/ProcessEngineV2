from django.contrib import admin
from .models import (
    ProcessDefinition,
    RegisteredTask,
    ProcessTask
)

class ProcessTasksInline(admin.TabularInline):
    model = ProcessTask

class ProcessDefinitionAdmin(admin.ModelAdmin):
    inlines = [ProcessTasksInline,]

admin.site.register(ProcessDefinition, ProcessDefinitionAdmin)
admin.site.register(RegisteredTask)
admin.site.register(ProcessTask)