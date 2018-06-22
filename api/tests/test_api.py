# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.test import TestCase
import json
from .testutils import (
    create_fake_definition_with_processes,
    create_fake_user
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

    def test_create_logged_in_user_adds_user_data_to_process(self):
        user = create_fake_user()
        self.client.login(username=user.username, password="testtest")
        result = self.client.post(self.url, self.data, format='json')

        actual_username = result.json().get('actor', {}).get('username')
        assert actual_username == user.username,\
            'Expected username to be: {} got: {}'.format(actual_username, user.username)

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