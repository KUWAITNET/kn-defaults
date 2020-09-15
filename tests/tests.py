from django.test import TestCase, override_settings
from django.urls import reverse
import pdb
import logging

from unittest.case import _AssertLogsContext, _BaseTestCaseContext, _CapturingHandler

from kn_defaults.logging.defaults import KN_FORMATTER, logging_decorator, FUNCTION_LOGGER_FORMATTER

_AssertLogsContext.LOGGING_FORMAT = KN_FORMATTER


class _AssertLogsContext(_BaseTestCaseContext):
    """A context manager used to implement TestCase.assertLogs()."""

    LOGGING_FORMAT = KN_FORMATTER  # "%{levelname}:%(name)s:%(message)s"

    def __init__(self, test_case, logger_name, level, logging_format="%{levelname}:%(name)s:%(message)s", style='%'):
        _BaseTestCaseContext.__init__(self, test_case)
        self.logger_name = logger_name
        if level:
            self.level = logging._nameToLevel.get(level, level)
        else:
            self.level = logging.INFO
        self.msg = None
        self.logging_format = logging_format or self.LOGGING_FORMAT
        self.format_style = style or '%'

    def __enter__(self):
        if isinstance(self.logger_name, logging.Logger):
            logger = self.logger = self.logger_name
        else:
            logger = self.logger = logging.getLogger(self.logger_name)
        formatter = logging.Formatter(self.logging_format, style=self.format_style)
        handler = _CapturingHandler()
        handler.setFormatter(formatter)
        self.watcher = handler.watcher
        self.old_handlers = logger.handlers[:]
        self.old_level = logger.level
        self.old_propagate = logger.propagate
        logger.handlers = [handler]
        logger.setLevel(self.level)
        logger.propagate = False
        return handler.watcher

    def __exit__(self, exc_type, exc_value, tb):
        self.logger.handlers = self.old_handlers
        self.logger.propagate = self.old_propagate
        self.logger.setLevel(self.old_level)
        if exc_type is not None:
            # let unexpected exceptions pass through
            return False
        if len(self.watcher.records) == 0:
            self._raiseFailure(
                "no logs of level {} or higher triggered on {}"
                    .format(logging.getLevelName(self.level), self.logger.name))


class KNLoggingTestCase(TestCase):
    def assertLogs(self, logger=None, level=None, formatter=None, style=None):
        """Fail unless a log message of level *level* or higher is emitted
        on *logger_name* or its children.  If omitted, *level* defaults to
        INFO and *logger* defaults to the root logger.

        This method must be used as a context manager, and will yield
        a recording object with two attributes: `output` and `records`.
        At the end of the context manager, the `output` attribute will
        be a list of the matching formatted log messages and the
        `records` attribute will be a list of the corresponding LogRecord
        objects.

        Example::

            with self.assertLogs('foo', level='INFO') as cm:
                logging.getLogger('foo').info('first message')
                logging.getLogger('foo.bar').error('second message')
            self.assertEqual(cm.output, ['INFO:foo:first message',
                                         'ERROR:foo.bar:second message'])
        """
        return _AssertLogsContext(self, logger, level, formatter, style)


class TestLogging(KNLoggingTestCase):

    def test_success_func_view(self):
        with self.assertLogs('kn_middleware_logger', 'INFO') as cm:
            self.client.get(reverse('success_func_view'))
        self.assertIn('took', cm.output[0])
        self.assertIn('META', cm.output[0])

    def test_logging_post_data_sensitive_parameters(self):
        with self.assertLogs('kn_middleware_logger', 'INFO') as cm:
            self.client.post(reverse('success_func_view'), data={'username': '<username>', 'password': 'secret'})
        self.assertIn('username', cm.output[0])
        self.assertNotIn('secret', cm.output[0])

    def test_options_api_call(self):
        with self.assertLogs('kn_middleware_logger', 'INFO') as cm:
            response = self.client.options(reverse('success_func_view'), data={'username': '<username>', 'password': 'secret'})
        self.assertEqual(response.status_code, 200)

    def test_error_func_view(self):

        with self.assertLogs('kn_middleware_logger', 'ERROR') as cm:
            try:
                self.client.get(reverse('error_func_view'), )
            except:
                pass
        self.assertIn(' error_func_view', cm.output[0].lower())
        self.assertIn('division by zero', cm.output[0].lower())

    def test_helper_log(self):
        def calling_function():
            from kn_defaults.logging.defaults import log
            data = {'sample_dict': True}
            var_a = 'long-variable-content-for-testing-var-a'
            var_b = 'long-variable-content-for-testing-var-b'

            log(10, 'Process is here')

        formatter = '{levelname}:{name} {asctime} {module} {process:d} {thread:d} {message} LocalVars: {vars} '
        with self.assertLogs('default', 'DEBUG', formatter, '{') as cm:
            calling_function()
        self.assertIn('long-variable-content-for-testing-var-a', cm.output[0])
        self.assertIn('long-variable-content-for-testing-var-b', cm.output[0])
        self.assertIn('sample_dict', cm.output[0])

    def test_logging_decorator_minimal(self):

        @logging_decorator
        def function_to_call(*args, **kwargs):
            return 'function_to_call_return_values'

        # formatter = '{levelname}:{name} {message}'
        # formatter = '{levelname}:{message} - args={args} kwargs={kwargs} return={return_value} '
        with self.assertLogs('kn_function_logger', 'DEBUG', FUNCTION_LOGGER_FORMATTER, '{') as cm:
            function_to_call('hello', from_the_other_side=True)

        self.assertIn('function_to_call_return_values', cm.output[0])
        self.assertIn('from_the_other_side', cm.output[0])
        self.assertIn('hello', cm.output[0])


class TestChecks(TestCase):

    @override_settings(LOGGING={})
    def test_adding_kn_defaults_logging(self):
        from kn_defaults.logging.checks import check_logging_settings
        errors = check_logging_settings()
        self.assertIsNotNone(errors, 'Check settings is not Ok')

    @override_settings(ROOT_URLCONF='tests.urls_w_default_admin')
    def test_admin(self):
        from kn_defaults.logging.checks import check_admin_url
        exception = check_admin_url(None)
        self.assertTrue(exception)
