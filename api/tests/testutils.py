from ..models import *
from django.contrib.auth import get_user_model

from faker import Factory
FAKE = Factory.create()

def create_fake_user(password="testtest", **kwargs):
    """Creates a fake user"""

    return get_user_model().objects.create_user(
        username=kwargs.get('username', FAKE.user_name()),
        email=kwargs.get('email', FAKE.email()),
        password=kwargs.get('password', password),
        first_name=kwargs.get('first_name', FAKE.first_name()),
        last_name=kwargs.get('last_name', FAKE.last_name()),
    )

def create_fake_registered_task(service, name):
    data = {
        "service": service,
        "method_to_call": name,
        "friendly_name": name,
    }
    if data is not None:
        data.update(data)

    return RegisteredTask.objects.create(**data)

def create_fake_scheduled_process_task(
        field = "obj.date",
        offset = 20,
        payload = {"obj": {"date": "2018-06-15T21:00:00"}}
    ):

    defn = create_fake_definition()
    registered_task = create_fake_registered_task("someservice", "sometask")

    process_task = ProcessTask()
    process_task.process_definition = defn
    process_task.registered_task = registered_task
    process_task.run_immediately = False
    process_task.schedule_offset_from_field = ["obj.date", str(offset)]
    process_task.payload_template = payload
    process_task.save()
    return process_task

def create_fake_offset_scheduled_process_task(offset = 20):

    defn = create_fake_definition()
    registered_task = create_fake_registered_task("someservice", "sometask")

    process_task = ProcessTask()
    process_task.process_definition = defn
    process_task.registered_task = registered_task
    process_task.run_immediately = False
    process_task.schedule_offset_from_now = offset
    process_task.payload_template = {}
    process_task.save()
    return process_task

def create_fake_definition():
    data = {
        "version": "1",
        "name": "test",
        "slug": "test",
        "example_payload": {"foo": "bar"}
    }
    return ProcessDefinition.objects.create(**data)

def create_fake_definition_with_processes():
    definition = create_fake_definition()
    # register a task
    registered_task = create_fake_registered_task("web", "ping")
    # connect the two
    ProcessTask.objects.create(
        process_definition = definition,
        registered_task = registered_task,
        payload_template = '{ "foo.bar": "{{foo.bar}}" }',
        runner = 'api.tasks.runners.http_task_runner'
    )
    return definition

def create_test_process_instance():
    '''
    Creates a process instance from scratch, including with
    ProcessDefinition and Registered task
    '''
    # create a definition
    definition = create_fake_definition_with_processes()

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

