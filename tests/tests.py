from django.test import TestCase
from django.urls import reverse
import pdb


class TestLogging(TestCase):

    def test_success_func_view(self):
        with self.assertLogs('kn_defaults', 'INFO') as cm:
            self.client.get(reverse('success_func_view'))

        # pdb.set_trace()
        self.assertIn('took', cm.output[0])
