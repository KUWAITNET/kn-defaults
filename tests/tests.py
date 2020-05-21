from django.test import TestCase
from django.urls import reverse
import pdb


class TestLogging(TestCase):

    def test_success_func_view(self):
        with self.assertLogs('kn_defaults', 'INFO') as cm:
            self.client.get(reverse('success_func_view'))
        self.assertIn('took', cm.output[0])

    def test_error_func_view(self):

        with self.assertLogs('kn_defaults', 'ERROR') as cm:
            try:
                self.client.get(reverse('error_func_view'),)
            except:
                pass
        # import pdb; pdb.set_trace()
        self.assertIn(' error_func_view', cm.output[0].lower())
        self.assertIn('division by zero', cm.output[0].lower())
