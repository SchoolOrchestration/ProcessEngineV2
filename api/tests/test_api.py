# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.test import TestCase
import json
from .testutils import (
    create_fake_definition,
    create_fake_definition_with_processes
)

class ProcessCreateTestCase(TestCase):

    def setUp(self):
        self.url = reverse('process-list')
        self.definition = create_fake_definition_with_processes()
        self.data = {
            "template": self.definition.name,
            "payload": json.dumps(self.definition.example_payload)
        }
        self.result = self.client.post(self.url, self.data)

    def test_create_with_json(self):
        result = self.client.post(self.url, self.data, format='json')
        assert result.status_code == 201,\
            'Expected 201. Got: {}'.format(result.status_code)

    def test_will_404_if_not_existing_template(self):
        data = {
            "template": "non existant definition"
        }
        result = self.client.post(self.url, data, format='json')

        assert result.status_code == 404,\
            'Expected 404. Got: {}'.format(result.status_code)

    def test_is_ok(self):
        assert self.result.status_code == 201, \
            'Expected 201. Got: {}'.format(self.result.status_code)