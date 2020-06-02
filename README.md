# kn-defaults

### Vision:

This project shall contains 

1. A Logging helper module in the form of Middleware, Decorator, and a helper function
2. A Utility collection that can help with everyday tasks 



### Installation:

You can install via `pip install -e git+git@github.com:KuwaitNET/kn-defaults.git#egg=django-kn-defaults`

### Components:

1. Logging Helpers
2. Checks
...

### Usage:

#### Logging Usage

* Add `kn_defaults.logging` to INSTALLED_APPS
* Add `'kn_defaults.logging.middlewares.KnLogging'` to your `MIDDLEWARE`
* Hook the logging configurations. (example below) 
* For middleware logging: Mark your url names to be logged by the setting `KN_LOGGING_URL_PATTERNS`


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

### Middleware logging Settings:

KN_LOGGING_URL_PATTERNS: a list of the url names to be logged by  the middleware. 
This list can accept a namespace url with an `*` to denote to log all urls under that namespace.
```python
KN_LOGGING_URL_PATTERNS = [
    'url_name',
    'namespace:url_name',
    'namespace2:*'
]
```

### The information being stored with the middleware logging

1. request_id : a unique if of the request to help traceback any logs accosiated with that specific request
2. method: GET/POST/ etc..
3. path: the request.path (ie url) which originated the log
4. ip
5. user: the request.user if the user is authenticated, None otherwise.
6. status_code: the response status code
7. outbound_payload: The plain response the view sent back
8. response_duration: How much time in seconds it took to generate a response back to the user
9. post_parameters: the POST information. This respects [Django's sensitive parameters decorator](https://docs.djangoproject.com/en/3.0/howto/error-reporting/#django.views.decorators.debug.sensitive_post_parameters) 


#### Logging Helper function:

Sample usage looks like this

```python
from kn_defaults.logging.defaults import log

log(level=10, msg='Message here')
```
The helper logging is ready for use out of the box.
It uses a handler called 'default', which logs all to '<CUR_DIR>/log.log'.
The log helper function also logs the local variables in the calling function.

For level names here is a map.
```python
CRITICAL = 50
ERROR = 40
WARNING = 30
INFO = 20
DEBUG = 10
```


#### function decorator Logging Helper:
```python
from kn_defaults.logging.defaults import logging_decorator

@logging_decorator(level=10, msg='')
def function(arg_1=True, *args, **kwargs):
    pass

```



## Helpers

1. `cms_plugin_change_admin_log` logs django-cms plugins addition/ update and delete to the regular admin log.
   In case of a change action, it logs the changed fields and their values before and after.
   It's automatically activated if 'cms' is in INSTALLED_APPS unless disabled by the setting `DISABLE_CMS_PLUGIN_CHANGE_ADMIN_LOG`
   



### Creating a release

The package version is controlled by kn_defaults.__init__.__version__ .
and preparing the sdist is by `python setup.py sdist`
