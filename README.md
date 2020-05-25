# kn-defaults

###Vision:

This project shall contains 

1. A Logging helper module in the form of Middleware, Decorator, and a helper function
2. A Utility collection that can help with everyday tasks 



###Usage:

* install `pip install -e git+git@github.com:KuwaitNET/kn-defaults.git#egg=django-kn-defaults`
* Add `kn_defaults.logging` to INSTALLED_APPS
* Add `'kn_defaults.logging.middlewares.KnLogging'` to your `MIDDLEWARE`
* Add `kn_defaults` to `SETTINGS.LOGGING`
* Mark your url names to be logged by the setting `KN_LOGGING_URL_PATTERNS`

###Logging Adjustments:

Because kn_defaults.logging logs many extra information around the log message itself, 
we need to add a formatter to the handler that is assigned to `kn_defaults` logger.

Below is a _minimalist_ sample that you can integrate with your already defined logging.

```python
from kn_defaults.logging.defaults import KN_FORMATTER
# the formatter format is rather long, it's in KN_FORMATTER, you can take a look at it.

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
        }
    }
}

```

###Settings:

KN_LOGGING_URL_PATTERNS: a list of the url names to be logged by  the middleware. 
This list can accept a namespace url with an `*` to denote to log all urls under that namespace.
```python
KN_LOGGING_URL_PATTERNS = [
    'url_name',
    'namespace:url_name',
    'namespace2:*'
]

```

###What are the information being stored with the logging

1. request_id : a unique if of the request to help traceback any logs accosiated with that specific request
2. method: GET/POST/ etc..
3. path: the request.path (ie url) which originated the log
4. ip
5. user: the request.user if the user is authenticated, None otherwise.
6. status_code: the response status code
7. outbound_payload: The plain response the view sent back
8. response_duration: How much time in seconds it took to generate a response back to the user
9. post_parameters: the POST information. This respects [Django's sensitive parameters decorator](https://docs.djangoproject.com/en/3.0/howto/error-reporting/#django.views.decorators.debug.sensitive_post_parameters) 

