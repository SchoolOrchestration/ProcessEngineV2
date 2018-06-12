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


def create_test_process_instance():
    '''
    Creates a process instance from scratch, including with
    ProcessDefinition and Registered task
    '''
    # create a definition
    definition = create_fake_definition()
    # register a task
    registered_task = create_fake_registered_task("web", "ping")
    # connect the two
    ProcessTask.objects.create(
        process_definition = definition,
        registered_task = registered_task,
        payload_template = '{ "foo.bar": "{{foo.bar}}" }'
    )

    payload = {
        "foo": {
            "bar": "hello!"
        }
    }
    return Process.from_definition(
        definition,
        owners=['1'],
        payload=payload
    )


"""

ProcessDefinition >-< RegisteredTasks

"""

