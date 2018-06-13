from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.template import Template, Context
import json, requests
'''
Other runners we might have:
- openwhisk
- lambda
- google functions
- azure functions
- pubsub
- ...
'''
TASK_RUNNERS = [
    ('api.tasks.http_task_runner', 'Trigger a task over HTTP'),
    ('api.tasks.local_task_runner', 'Call a locally available task'),
]

TASK_STATUSES = [
    ('N', 'New'),
    ('IP', 'In Progress'),
    ('C', 'Complete'),
    ('F', 'Failed'),
    ('X', 'Cancelled'),
]

REGISTERED_TASK_STATUSES = [
    ('alpha', 'alpha'),
    ('beta', 'beta'),
    ('stable', 'stable'),
]

class RegisteredTask(models.Model):
    '''
    Registered tasks are tasks that are available.
    Registered tasks attacked to a ProcessDefinition are used to
    '''
    def __str__(self):
        return "{}.{}".format(self.service, self.name)

    service = models.CharField(max_length=255, blank=True, null=True, help_text='This is downstream service to call')
    name = models.CharField(max_length=255, blank=True, null=True, help_text='This is the formal name of the test that will be called')
    friendly_name = models.CharField(max_length=255, blank=True, null=True)
    registered_runners = ArrayField(models.CharField(max_length=100), default=[], db_index=True, help_text='A list of the runners available for this task')
    production_status = models.CharField(max_length=10, choices=REGISTERED_TASK_STATUSES, default='alpha')
    docs = models.TextField(blank=True, null=True, help_text='Markdown is supported')
    example_payload = JSONField(default={}, blank=True, null=True)
    example_response = JSONField(default={}, blank=True, null=True)

class ProcessDefinition(models.Model):
    '''
    This is where you can define how a process will act
    '''

    object_ids = ArrayField(models.CharField(max_length=100), default=[], db_index=True)

    version = models.CharField(max_length=10, db_index=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50)
    docs = models.TextField(blank=True, null=True, help_text='Markdown is supported')
    example_payload = JSONField(default={}, blank=True, null=True)
    example_response = JSONField(default={}, blank=True, null=True)
    is_live = models.BooleanField(default=False, help_text='Whether or not this process is publically available')

    tasks = models.ManyToManyField(RegisteredTask, through='ProcessTask')


class ProcessTask(models.Model):
    '''
    This joining table defines how tasks will act for a given process definition.
    e.g.: the details for how a task is run may vary from process to process - those differences are recorded here
    This is basically where we keep the invokation information for a task instance in a process
    '''
    process_definition = models.ForeignKey(ProcessDefinition, on_delete=models.CASCADE)
    registered_task = models.ForeignKey(RegisteredTask, on_delete=models.SET_NULL, null=True)

    runner = models.CharField(max_length=50, choices=TASK_RUNNERS)
    run_immediately = models.BooleanField(default=True, help_text='Will run this task immediately and include the result in the response to the upstream process')
    is_async = models.BooleanField(default=False, help_text='Run this task in the background (Response is not returned in realtime)')

    payload_template = JSONField(default={}, help_text='A jinja/django template which will be parsed with the context from the parent process to create the payload for the task to be run')

    # only one of these can be set (and run_immediately must be false)
    schedule_offset_from_now = models.PositiveIntegerField(default=0, help_text='Offset in seconds from now', db_index=True)
    schedule_offset_from_field = ArrayField(models.CharField(max_length=100), default=[], db_index=True, help_text='A tuple in the format: ["payload.object.date_created", "60"]')


class Process(models.Model):
    '''
    POST /process/:version/ --data-binary '{ "name": ..., payload: {} }'
    '''

    owners = ArrayField(models.CharField(max_length=100), default=[], db_index=True, help_text='object keys for objects that are allowed to act on this process')
    object_ids = ArrayField(models.CharField(max_length=100), default=[], db_index=True)

    definition = models.ForeignKey(ProcessDefinition, on_delete=models.SET_NULL, null=True) # required
    payload = JSONField(default={})

    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True, db_index=True)

    @classmethod
    def from_definition(cls, definition, owners, payload, task_payload_templates = {}, object_ids=[], with_save=True):
        instance = cls()
        instance.owners = owners
        instance.object_ids = owners
        instance.definition = definition
        instance.payload = payload
        if with_save: instance.save()

        for task in definition.processtask_set.all():
            task = Task.from_process_task(instance, task)

        return instance


    def run(self, force = False):
        '''
        Run all pending downstream tasks
        Use force to re-run/force-run all downstream methods
        '''
        for task in self.task_set.all():
            task.run()

        return self

class Task(models.Model):
    '''
    A work item to be performed
    '''
    process = models.ForeignKey(Process, blank=True, null=True, on_delete=models.CASCADE)
    definition = models.ForeignKey(RegisteredTask, on_delete=models.SET_NULL, null=True)
    service = models.CharField(max_length=100, help_text='This is downstream service to call')
    method_name = models.CharField(max_length=100, help_text='This is the formal name of the test that will be called')
    friendly_name = models.CharField(max_length=100, blank=True, null=True)

    payload = JSONField(default={})

    runner = models.CharField(max_length=10, choices=TASK_RUNNERS)
    status = models.CharField(max_length=10, choices=TASK_STATUSES, default='N')

    run_immediately = models.BooleanField(default=True, help_text='Will run this task immediately and include the result in the response to the upstream process')
    scheduled_datetime = models.DateTimeField(db_index=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True, db_index=True)

    def run(self):
        """
        result = tasks.runners.call(self.runner, self.service, self.task, self.payload)
        """
        url = "http://{}/tasks/".format(self.service)
        data = {
            "task": self.method_name,
            "payload": self.payload
        }
        result = requests.post(url, data)
        Result.from_run_result(self, result)
        return result

    @classmethod
    def from_process_task(cls, process, task_template, with_save=True, **config):
        instance = cls()
        instance.process = process
        instance.definition = task_template.registered_task
        instance.service = task_template.registered_task.service
        instance.method_name = task_template.registered_task.name

        template = Template(task_template.payload_template)
        rendered_payload = template.render(context=Context(process.payload))

        instance.payload = json.loads(rendered_payload)
        for key,value in config.items():
            setattr(instance, key, value)
        if with_save:
            instance.save()
        return instance


class Result(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    response = JSONField(default={})
    response_code = models.CharField(max_length=10, default='0')
    is_success_response = models.BooleanField(default=False)

    @classmethod
    def from_run_result(cls, task, result, with_save=True):
        instance = cls()
        instance.task = task
        instance.is_success_response = result.status_code < 300
        instance.response = result.json()
        instance.response_code = result.status_code

        if with_save: instance.save()
        return instance