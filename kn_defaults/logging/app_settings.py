from django.conf import settings
from django.utils.functional import lazy

KN_LOGGING_URL_PATTERNS = lazy(lambda: getattr(settings, 'KN_LOGGING_URL_PATTERNS', []), list)()
