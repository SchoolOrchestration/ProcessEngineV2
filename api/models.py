from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

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
    service = models.TextField(blank=True, null=True, help_text='This is downstream service to call')
    name = models.TextField(blank=True, null=True, help_text='This is the formal name of the test that will be called')
    friendly_name = models.TextField(blank=True, null=True)
    registered_runners = ArrayField(models.CharField(max_length=100), default=[], db_index=True, help_text='A list of the runners available for this task')
    production_status = models.CharField(max_length=10, choices=REGISTERED_TASK_STATUSES, default='alpha')

class ProcessDefinition(models.Model):
    '''
    This is where you can define how a process will act
    '''

    object_ids = ArrayField(models.CharField(max_length=100), default=[], db_index=True)

    version = models.CharField(max_length=10, db_index=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50)
    docs = models.TextField(blank=True, null=True, help_text='Markdown is supported')
    example_payload = JSONField(default={})
    example_response = JSONField(default={})
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

    runner = models.CharField(max_length=10, choices=TASK_RUNNERS)
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

    def __str__(self):
        return 'Settings for Practitioner #{}'.format(self.practitioner_id)

    owners = ArrayField(models.CharField(max_length=100), default=[], db_index=True, help_text='object keys for objects that are allowed to act on this process')
    object_ids = ArrayField(models.CharField(max_length=100), default=[], db_index=True)

    definition = models.ForeignKey(ProcessDefinition, on_delete=models.SET_NULL, null=True) # required
    payload = JSONField(default={})

    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True, db_index=True)

    def run(self):
        '''
        Run all pending downstream tasks
        '''
        pass

    def on_create(self):
        '''
        Prepare and run all downstream tasks
        '''
        registered_tasks = self.definition.registered_tasks
        for registered_task in registered_tasks:
            Task.from_registered_task(task)


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

    def call(self):
        """
        result = tasks.runners.call(self.runner, self.service, self.task, self.payload)
        """
        pass

    @classmethod
    def from_registered_task(self):
        pass

class Result(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    response = JSONField(default={})
    response_code = models.CharField(max_length=10, default='0')
    is_success_response = models.BooleanField(default=False)