from ..models import *

def create_fake_registered_task(service, name):
    data = {
        "service": service,
        "name": name,
        "friendly_name": name,
    }
    if data is not None:
        data.update(data)

    return RegisteredTask.objects.create(**data)


def create_fake_definition():
    data = {
        "version": "1",
        "name": "test",
        "slug": "test"
    }
    return ProcessDefinition.objects.create(**data)

"""

ProcessDefinition >-< RegisteredTasks

"""

