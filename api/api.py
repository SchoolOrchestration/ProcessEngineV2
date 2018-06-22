'''
Main API
'''
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import routers, viewsets, response, exceptions
import json, jsonschema

from .helpers import (
    get_tasks_by_module_string,
    call_method_from_string
)
from .serializers import (
    ProcessSerializer,
    ProcessDefinitionSerializer,
    RegisteredTaskSerializer,
    UserSerializer
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
    queryset = Process.objects.all().order_by('-created_date')

    def __validate_payload(self):
        try:
            jsonschema.validate(self.schema, self.payload)
        except jsonschema.exceptions.ValidationError as e:
            msg = e.message.format(e.context)
            raise exceptions.ValidationError(msg)

    def create(self, request):
        """
        Create a process from the provided template:

        ```
        POST /process/
        {
            template: 'process-slug',
            payload: {...}
        }
        ```
        """
        template = request.data.get('template')
        payload = request.data.get('payload', {})
        if not isinstance(payload, dict):
            payload = json.loads(payload)
        definition = get_object_or_404(ProcessDefinition, slug=template)

        actor = None
        if request.user:
            if request.user.is_authenticated:
                actor = UserSerializer(request.user).data
        process = Process.from_definition(definition, ["1"], payload, actor)
        process.run()
        result = ProcessSerializer(process).data
        return response.Response(result, status=201)


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'process-definitions', ProcessDefinitionViewSet)
router.register(r'registered-tasks', RegisteredTaskViewSet)
router.register(r'process', ProcessViewSet)