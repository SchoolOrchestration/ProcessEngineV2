from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.template import Template, Context
from datetime import datetime, timedelta
from django.utils import timezone
from dateutil.parser import parse
import json, requests, pytz

from .tasks.runners import call
from .helpers import get_object_path

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
    ('api.tasks.runners.http_task_runner', 'Trigger a task over HTTP'),
    # ('api.tasks.runners.local_task_runner', 'Call a locally available task'),
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

class RegisteredService(models.Model):
    '''
    Registered services represent services connected to this process engine
    Exposed tasks from registered services can be discovered and made into
    registered tasks for this process engine
    '''
    def __str__(self):
        return self.name

    name = models.CharField(max_length=255, help_text='This is the formal name of the test that will be called')
    base_url = models.CharField(max_length=255, blank=True, null=True, help_text='The internal base url where this service can be found')
    api_key = models.CharField(max_length=255, blank=True, null=True, help_text='If your task endpoint requires an API key, specify it here. API key can be sent via params or Authorization Bearer')
    channel = models.CharField(max_length=255, blank=True, null=True, help_text='A channel on which this service is listening')

class RegisteredTask(models.Model):
    '''
    Registered tasks are tasks that are available.
    Registered tasks attacked to a ProcessDefinition are used to
    '''
    def __str__(self):
        return "{}:{}".format(self.service, self.method_to_call)

    service = models.CharField(max_length=255, blank=True, null=True, help_text='This is downstream service to call')
    friendly_name = models.CharField(max_length=255, blank=True, null=True)
    method_to_call = models.CharField(max_length=255, blank=True, null=True, help_text='Full path to the method to call. e.g.: `api.tasks.ping`')

    registered_runners = ArrayField(models.CharField(max_length=100), default=[], db_index=True, help_text='A list of the runners available for this task')
    production_status = models.CharField(max_length=10, choices=REGISTERED_TASK_STATUSES, default='alpha')
    docs = models.TextField(blank=True, null=True, help_text='Markdown is supported')
    example_payload = JSONField(default={}, blank=True, null=True)
    example_response = JSONField(default={}, blank=True, null=True)

    def health_check(self):
        '''
        As configured, verify that the task exists upstream and
        is available
        '''

class ProcessDefinition(models.Model):
    '''
    This is where you can define how a process will act
    '''
    def __str__(self):
        return "{} ()".format(self.name, self.version)

    object_ids = ArrayField(models.CharField(max_length=100), default=[], db_index=True)

    version = models.CharField(max_length=10, db_index=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50)
    docs = models.TextField(blank=True, null=True, help_text='Markdown is supported')
    schema = JSONField(default={}, blank=True, null=True, help_text='Define what the payload should look like using a jsonschema. If provided, this will be used for validation')
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
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    process_definition = models.ForeignKey(ProcessDefinition, on_delete=models.CASCADE)
    registered_task = models.ForeignKey(RegisteredTask, on_delete=models.SET_NULL, null=True)

    runner = models.CharField(max_length=50, choices=TASK_RUNNERS, default='api.tasks.runners.http_task_runner')
    is_async = models.BooleanField(default=False, help_text='Run this task in the background (Response is not returned in realtime)')

    payload_template = JSONField(default={}, blank=True, null=True, help_text='A jinja/django template which will be parsed with the context from the parent process to create the payload for the task to be run')

    # scheduling:
    # priority is top to bottom: e.g.: run_immediately, from_now, from_field
    # from_now == 0 means it will be skipped and we'll evaluate offset_from_field
    run_immediately = models.BooleanField(default=True, help_text='Will run this task immediately and include the result in the response to the upstream process')
    schedule_offset_from_now = models.PositiveIntegerField(default=0, help_text='Offset in seconds from now', db_index=True)
    schedule_offset_from_field = ArrayField(
        models.CharField(max_length=100), default=[], db_index=True, help_text='A tuple in the format: ["payload.object.date_created", "60"]',
        blank=True, null=True
    )


class Process(models.Model):
    '''
    POST /process/:version/ --data-binary '{ "name": ..., payload: {} }'
    '''

    def __str__(self):
        return "Instance of: {}".format(self.definition)

    actor = JSONField(default={}, blank=True, null=True)
    owners = ArrayField(models.CharField(max_length=100), default=[], db_index=True, blank=True, null=True, help_text='object keys for objects that are allowed to act on this process')
    object_ids = ArrayField(models.CharField(max_length=100), default=[], blank=True, null=True, db_index=True)

    definition = models.ForeignKey(ProcessDefinition, on_delete=models.SET_NULL, null=True) # required
    payload = JSONField(default={}, blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True, db_index=True)

    @classmethod
    def from_definition(cls, definition, owners, payload, actor = None, object_ids=[], with_save=True):
        instance = cls()
        instance.owners = owners
        instance.actor = actor
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
            if not force and task.should_run():
                task.run()

        return self

class Task(models.Model):
    '''
    A work item to be performed
    '''
    def __str__(self):
        return "[{}] {}: {}".format(self.definition, self.service, self.method_name)

    process = models.ForeignKey(Process, blank=True, null=True, on_delete=models.CASCADE)
    definition = models.ForeignKey(ProcessTask, on_delete=models.SET_NULL, null=True)
    service = models.CharField(max_length=100, help_text='This is downstream service to call')
    method_name = models.CharField(max_length=100, help_text='This is the formal name of the test that will be called')
    friendly_name = models.CharField(max_length=100, blank=True, null=True)

    payload = JSONField(default={})

    runner = models.CharField(max_length=50, choices=TASK_RUNNERS)
    status = models.CharField(max_length=10, choices=TASK_STATUSES, default='N')

    run_immediately = models.BooleanField(default=True, help_text='Will run this task immediately and include the result in the response to the upstream process')
    scheduled_datetime = models.DateTimeField(db_index=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True, db_index=True)


    def should_run(self):
        if self.run_immediately: return True

        if self.scheduled_datetime <= timezone.now():
            return True


    def run(self):
        """
        result = tasks.runners.call(self.runner, self.service, self.task, self.payload)
        """
        self.status = 'IP'
        self.save()
        try:
            (result, is_success) = call(self.runner, self)
        except Exception as e:
            is_success = False
            result = e.message

        if is_success:
            self.status = 'C'
        else:
            self.status = 'F'
        self.save()
        Result.from_run_result(self, result)

        return result

    def __set_schedule(self):
        if self.definition.run_immediately: return True

        if self.definition.schedule_offset_from_field is not None and \
            len(self.definition.schedule_offset_from_field) == 2 \
            and self.definition.schedule_offset_from_now == 0:
            field_name, time_offset = self.definition.schedule_offset_from_field

            field_value = get_object_path(self.process.payload, field_name)
            dt_value = parse(field_value)
            dt = dt_value + timedelta(minutes=int(time_offset))
            if timezone.is_naive(dt):
                # naive datetimes get utc'ed
                dt = timezone.make_aware(dt, pytz.utc)
            self.run_immediately = False
            self.scheduled_datetime = dt

        if self.definition.schedule_offset_from_now > 0:
            now = datetime.utcnow()
            offset = timedelta(minutes=self.definition.schedule_offset_from_now)
            dt = timezone.make_aware((now + offset), pytz.utc)
            self.run_immediately = False
            self.scheduled_datetime = dt

    def __set_payload(self):
        pass

    def __set_fields(self, config):
        pass

    @classmethod
    def from_process_task(cls, process, task_template, with_save=True, **config):
        instance = cls()
        instance.process = process
        registered_task = task_template.registered_task
        instance.definition = task_template
        instance.service = registered_task.service
        instance.method_name = registered_task.method_to_call
        instance.runner = task_template.runner

        template_string = task_template.payload_template
        if not isinstance(template_string, str):
            template_string = json.dumps(template_string)
        template = Template(template_string)
        rendered_payload = template.render(context=Context(process.payload))

        instance.payload = json.loads(rendered_payload)
        for key,value in config.items():
            setattr(instance, key, value)

        instance.__set_schedule()

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
        instance.is_success_response = result.ok
        if result.ok:
            instance.response = result.json()
        else:
            try:
                instance.response = result.json()
            except json.decoder.JSONDecodeError:
                instance.response = {
                    "error": result.content.decode("utf-8")
                }
        instance.response_code = result.status_code

        if with_save: instance.save()
        return instance