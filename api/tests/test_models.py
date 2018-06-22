# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.utils import timezone

from .testutils import (
    create_test_process_instance,
    create_fake_scheduled_process_task,
    create_fake_offset_scheduled_process_task
)
from ..models import (
    Process,
    Task
)
from datetime import datetime
import responses, pytz

class ProcessTestCase(TestCase):

    def setUp(self):
        self.process = create_test_process_instance()

    def test_payload_is_correctly_parsed(self):
        task = self.process.task_set.first()
        assert task.payload.get("foo.bar") == "hello!"

    @responses.activate
    def test_run_process(self):

        responses.add(
            responses.POST,
            'http://web/tasks/',
            json={'message': 'pong'},
            status=201
        )

        process = self.process.run()

class ScheduledTaskTestCase(TestCase):

    def setUp(self):
        process = create_test_process_instance()
        process.payload = {
            "obj": {
                "date": "2018-06-15T21:00:00+02:00"
            }
        }
        process.save()
        self.process_task = create_fake_scheduled_process_task(
                                field = "obj.data",
                                offset = 20
                            )
        self.task = Task.from_process_task(process, self.process_task)

    def test_it_sets_the_scheduled_date(self):
        actual = self.task.scheduled_datetime.isoformat()
        expected = '2018-06-15T21:20:00+02:00'
        assert actual == expected, 'Expected {} to be {}'.format(actual, expected)

class ScheduledNowOffsetTaskTestCase(TestCase):

    def setUp(self):
        process = create_test_process_instance()
        process.save()
        self.process_task = create_fake_offset_scheduled_process_task(offset = 20)
        self.task = Task.from_process_task(process, self.process_task)

    def test_it_sets_the_scheduled_date(self):
        actual = self.task.scheduled_datetime
        delta = timezone.make_aware(datetime.utcnow(), pytz.utc) - actual

        assert delta.total_seconds() < 60, \
            'Time should be now + 20mins. But got: {}'.format(actual)

