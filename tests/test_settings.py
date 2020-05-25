import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'kn_defaults.logging',
    "tests",
]

ROOT_URLCONF = 'tests.urls'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'kn_defaults.logging.middlewares.KnLogging']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test.sqlite3'),
    }
}

KN_LOGGING_URL_PATTERNS = [
    'success_func_view',
    'error_func_view',
]
from kn_defaults.logging.defaults import KN_FORMATTER

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose_kn': {
            'format': KN_FORMATTER,
        },
    },
    'handlers': {
        'kn_default_handler': {
            'formatter': 'verbose_kn'
        },
    },
    'loggers': {
        'kn_defaults': {
            'handlers': ['kn_default_handler'],
            'level': 'INFO',
        }
    }
}

