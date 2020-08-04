from django.conf import settings
from django.utils.functional import lazy
import os

KN_LOGGING_URL_PATTERNS = lazy(lambda: getattr(settings, 'KN_LOGGING_URL_PATTERNS', []), list)()
DISABLE_CMS_PLUGIN_CHANGE_ADMIN_LOG = lazy(lambda: getattr(settings, 'DISABLE_CMS_PLUGIN_CHANGE_ADMIN_LOG', False),
                                           bool)()
KN_LOG_FILE_SIZE = lazy(lambda: getattr(settings, 'KN_LOG_FILE_SIZE', 5 * 1024 * 1024), int)()
KN_HANDLER_CLASS = lazy(
    lambda: getattr(settings, 'KN_HANDLER_CLASS', 'logging.handlers.RotatingFileHandler'), str)()
KN_LOG_FILE_PATH = lazy(
    lambda: getattr(settings, 'KN_LOG_FILE_PATH', os.path.join(os.getcwd(), 'log.log')), str)()
KN_LOG_BACKUP_COUNT = lazy(lambda: getattr(settings, 'KN_LOG_BACKUP_COUNT', 3), int)()
KN_PRODUCTION = lazy(lambda: getattr(settings, 'KN_PRODUCTION', not settings.DEBUG), bool)()
