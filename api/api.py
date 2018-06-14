'''
Main API
'''
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import routers, viewsets, response
import json

from .helpers import (
    get_tasks_by_module_string,
    call_method_from_string
)
from .serializers import (
    ProcessSerializer,
    ProcessDefinitionSerializer,
    RegisteredTaskSerializer
)
from .models import (
    Process,
    ProcessDefinition,
    RegisteredTask
)

class ProcessDefinitionViewSet(viewsets.ModelViewSet):
    serializer_class = ProcessDefinitionSerializer
    queryset = ProcessDefinition.objects.all()

class RegisteredTaskViewSet(viewsets.ModelViewSet):
    serializer_class = RegisteredTaskSerializer
    queryset = RegisteredTask.objects.all()

class ProcessViewSet(viewsets.ModelViewSet):
    serializer_class = ProcessSerializer
    queryset = Process.objects.all()

    def create(self, request):
        name = request.data.get('name')
        payload = json.loads(request.data.get('payload', {}))
        definition = ProcessDefinition.objects.get(name=name)
        process = Process.from_definition(definition, ["1"], payload)
        import ipdb;ipdb.set_trace()
        process.run()
        result = ProcessSerializer(process).data
        return response.JSONResponse(result)

class TaskViewSet(viewsets.ViewSet):
    """
    Viewset for upstream microservices which exposes tasks
    over API (not intended to be available outside the internal network)
    """

    def list(self, request):
        all_tasks = []
        for module_string in settings.ALLOWED_TASK_MODULES:
            tasks = get_tasks_by_module_string(module_string)
            all_tasks += tasks
        return response.Response(all_tasks)

    def create(self, request, pk=None):
        """
        Create a task

        POST /task/:method/ --data payload
        """
        task = request.data.get('task')
        data = request.data.get('payload')
        result = call_method_from_string(task, data)
        return response.Response(result)


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, base_name='task')
router.register(r'process-definitions', ProcessDefinitionViewSet)
router.register(r'registered-tasks', RegisteredTaskViewSet)
router.register(r'process', ProcessViewSet)