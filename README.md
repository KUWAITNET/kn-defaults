# kn-defaults

### Vision:

This project shall contains 

1. A Logging helper module in the form of Middleware, Decorator, and a helper function
2. A Utility collection that can help with everyday tasks 



### Installation:

You can install via `pip install -e git+git@github.com:KuwaitNET/kn-defaults.git#egg=django-kn-defaults`

### Usage:

* Add `kn_defaults.logging` to INSTALLED_APPS
* Add `'kn_defaults.logging.middlewares.KnLogging'` to your `MIDDLEWARE`
* Adjust the logging configurations.
* Mark your url names to be logged by the setting `KN_LOGGING_URL_PATTERNS`

### Logging Adjustments:

You can do that by simply integrating the kn BASE_LOGGING dict with your project.

```python
from kn_defaults.logging.defaults import BASE_LOGGING

BASE_LOGGING.update({
        # Your extra logging configurations goes here
        })

LOGGING = BASE_LOGGING
```
If you have a logging config already, you can merge it with BASE_LOGGING by hand.
Check `kn_defaults.logging.defaults` for information

### Settings:

KN_LOGGING_URL_PATTERNS: a list of the url names to be logged by  the middleware. 
This list can accept a namespace url with an `*` to denote to log all urls under that namespace.
```python
KN_LOGGING_URL_PATTERNS = [
    'url_name',
    'namespace:url_name',
    'namespace2:*'
]

```

### What are the information being stored with the logging

1. request_id : a unique if of the request to help traceback any logs accosiated with that specific request
2. method: GET/POST/ etc..
3. path: the request.path (ie url) which originated the log
4. ip
5. user: the request.user if the user is authenticated, None otherwise.
6. status_code: the response status code
7. outbound_payload: The plain response the view sent back
8. response_duration: How much time in seconds it took to generate a response back to the user
9. post_parameters: the POST information. This respects [Django's sensitive parameters decorator](https://docs.djangoproject.com/en/3.0/howto/error-reporting/#django.views.decorators.debug.sensitive_post_parameters) 

