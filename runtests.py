# !/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
    os.environ['DJANGO_PROJECT_NAME'] = 'kn_defaults_test'
    os.environ['DJANGO_PROJECT_ROOT'] = '.'
    os.environ['DJANGO_LOGSTASH_HOST'] = ''
    os.environ['DJANGO_LOGSTASH_PORT'] = '0'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests"])
    sys.exit(bool(failures))
