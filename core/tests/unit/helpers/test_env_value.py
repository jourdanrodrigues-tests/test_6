import os

from django.test import SimpleTestCase

from core.helpers import EnvValue

ENV_KEY = 'TEST'


class TestToBool(SimpleTestCase):
    def test_when_zero_is_the_value_then_returns_false(self):
        os.environ[ENV_KEY] = '0'
        self.assertFalse(EnvValue(ENV_KEY).to_bool())

    def test_when_one_is_the_value_then_returns_true(self):
        os.environ[ENV_KEY] = '1'
        self.assertTrue(EnvValue(ENV_KEY).to_bool())
