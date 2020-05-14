from django.conf import settings
from django.urls import reverse
KN_LOGGING_URL_PATTERNS = getattr(settings, 'KN_LOGGING_URL_PATTERNS', [])
"""
patterns can hold such strings
- '*' log everything on the website
- 'urlname' log that url-name
- 'namespace:*' logs everything under that url namespace

You can exclude patterns by adding a '-' in front of the urlname/pattern
 
"""

