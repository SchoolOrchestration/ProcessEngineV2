# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from ..helpers import get_object_path

class HelpersTestCase(TestCase):

    def test_get_object_path(self):
        obj = {
            "foo": {
                "bar": {
                    "baz": "bus"
                }
            }
        }
        result = get_object_path(obj, "foo.bar.baz")
        assert result == "bus",\
            'Expected bus, got: {}'.format(result)