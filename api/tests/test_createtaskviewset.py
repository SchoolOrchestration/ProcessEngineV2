# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.test import TestCase

from ..api import (
    call_method_from_string
)


class ListTaskTestCase(TestCase):

    def setUp(self):
        url = reverse('task-list')
        self.result = self.client.get(url)

    def test_get_tasks(self):
        assert self.result.status_code == 200

class RunTaskTestCase(TestCase):

    def setUp(self):
        data = {
            'task': 'api.tasks.tasks.ping'
        }
        url = reverse('task-list')
        self.result = self.client.post(url, data)

    def test_call_method_from_string(self):

        result = call_method_from_string('api.tasks.tasks.ping')
        assert result.get("message") == "pong"

    def test_invoke_method_over_http(self):
        assert self.result.status_code == 200

    def test_only_allows_to_call_from_allowed_locations(self):
        pass

    def test_lists_all_available_tasks(self):
        pass



