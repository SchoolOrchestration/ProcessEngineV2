# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from ..models import (
    Process,
    Task,
    ProcessTask
)
from .testutils import (
    create_fake_definition,
    create_fake_registered_task
)

class ProcessTestCase(TestCase):

    def setUp(self):
        self.definition = create_fake_definition()
        self.registered_task = create_fake_registered_task("localhost", "ping")

        ProcessTask.objects.create(
            process_definition = self.definition,
            registered_task = self.registered_task,
            payload_template = '{"foo.bar": "{{foo.bar}}'
        )

        payload = {
            "foo": {
                "bar": "hello!"
            }
        }
        task_payload_templates = {
            "ping": {
                "message": "{{foo.bar}}"
            }
        }
        self.process = Process.from_definition(
            self.definition,
            owners=['1'],
            payload=payload,
            task_payload_templates=task_payload_templates
        )

    def test_payload_is_correctly_parse(self):
        task = self.process.task_set.first()
        import ipdb;ipdb.set_trace()
        assert task.payload.get("message") == "hello!"


