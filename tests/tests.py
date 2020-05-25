from django.test import TestCase, override_settings
from django.urls import reverse
import pdb

from unittest.case import _AssertLogsContext

from kn_defaults.logging.defaults import KN_FORMATTER

_AssertLogsContext.LOGGING_FORMAT = KN_FORMATTER


class TestLogging(TestCase):

    def test_success_func_view(self):
        with self.assertLogs('kn_defaults', 'INFO') as cm:
            self.client.get(reverse('success_func_view'))
        self.assertIn('took', cm.output[0])

    def test_logging_post_data_sensitive_parameters(self):
        with self.assertLogs('kn_defaults', 'INFO') as cm:
            self.client.post(reverse('success_func_view'), data={'username': '<username>', 'password': 'secret'})
        self.assertIn('username', cm.output[0])
        self.assertNotIn('secret', cm.output[0])

    def test_error_func_view(self):

        with self.assertLogs('kn_defaults', 'ERROR') as cm:
            try:
                self.client.get(reverse('error_func_view'), )
            except:
                pass
        self.assertIn(' error_func_view', cm.output[0].lower())
        self.assertIn('division by zero', cm.output[0].lower())


@override_settings(LOGGING={})
class TestChecks(TestCase):
    def test_adding_kn_defaults_logging(self):
        from kn_defaults.logging.checks import check_logging_settings
        errors = check_logging_settings()
        self.assertIsNotNone(errors, 'Check settings is not Ok')
