from django.conf import settings
from django.utils.functional import lazy

KN_LOGGING_URL_PATTERNS = lazy(lambda: getattr(settings, 'KN_LOGGING_URL_PATTERNS', []), list)()
DISABLE_CMS_PLUGIN_CHANGE_ADMIN_LOG = lazy(lambda: getattr(settings, 'DISABLE_CMS_PLUGIN_CHANGE_ADMIN_LOG', False), bool)()
KN_LOG_FILE_SIZE = lazy(lambda: getattr(settings, 'KN_LOG_FILE_SIZE', 5 * 1024 * 1024), int)()