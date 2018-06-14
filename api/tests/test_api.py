# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.test import TestCase

from .testutils import (
    create_fake_definition,
    create_fake_definition_with_processes
)

class ProcessCreateTestCase(TestCase):

    def setUp(self):
        url = reverse('process-list')
        definition = create_fake_definition_with_processes()
        data = {
            "name": definition.name,
            "payload": definition.example_payload
        }
        self.result = self.client.post(url)

    def test_is_ok(self):

        assert self.result.status_code == 201, \
            'Expected 201. Got: {}'.format(self.result.status_code)