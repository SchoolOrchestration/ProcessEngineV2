# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .testutils import create_test_process_instance
import responses

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


