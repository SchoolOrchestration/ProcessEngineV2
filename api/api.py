from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import routers, serializers, viewsets, response
import importlib

def call_method_from_string(method_string, payload = None):
    '''
    given a string path, call the method
    '''
    parts = method_string.split('.') # qualified method: e.g.: api.tasks.ping
    method_to_call = parts.pop()
    module_string = ('.').join(parts)
    module = importlib.import_module(module_string)
    func = getattr(module, method_to_call)
    return func(payload)

def get_tasks_by_module_string(module_string):
    module = importlib.import_module(module_string)
    tasks = []
    for method_string in dir(module):
        method = getattr(module, method_string)
        if callable(method):
            tasks.append({
                "name": method_string,
                "docs": method.__doc__
            })
    return tasks


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