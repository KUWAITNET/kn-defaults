import copy
from functools import wraps
import logging
import os
import environ

env = environ.Env()

logger = logging.getLogger("default")

KN_FORMATTER = (
    "%(levelname)s:%(name)s; "
    "REQ_id:%(request_id)s; %(message)s; path=%(path)s; method=%(method)s;ip=%(ip)s; "
    "status_code:%(status_code)s; response_duration:%(response_duration)s; "
    "post_parameters: %(post_parameters)s; outbound:%(outbound_payload)s; META: %(meta)s"
)

FUNCTION_LOGGER_FORMATTER = "{levelname}:{message} - args={func_args} kwargs={func_kwargs} return={func_return_value} "
PROJECT_NAME = env.str("DJANGO_PROJECT_NAME")
PROJECT_ROOT = env.str("DJANGO_PROJECT_ROOT")
LOGSTASH_HOST = env.str("DJANGO_LOGSTASH_HOST")
LOGSTASH_PORT = env.int("DJANGO_LOGSTASH_PORT")

LOGSTASH_ENV = env.str("DJANGO_LOGSTASH_ENV", "dev")
LOGSTASH_EXTRA_PREFIX = env.str("DJANGO_LOGSTASH_EXTRA_PREFIX", "dev")
LOGSTASH_SSL_ENABLE = env.bool("DJANGO_LOGSTASH_SSL_ENABLE", False)

BASE_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "logstash": {
            "()": "logstash_async.formatter.DjangoLogstashFormatter",
            "message_type": "python-logstash",
            "fqdn": False,
            "extra_prefix": LOGSTASH_EXTRA_PREFIX,
            "extra": {
                "application": PROJECT_NAME,
                "project_path": PROJECT_ROOT,
                "environment": LOGSTASH_ENV,
            },
        },
        "verbose": {
            "format": "{name} {levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "logstash": {
            "level": "DEBUG",
            "class": "logstash_async.handler.AsynchronousLogstashHandler",
            "formatter": "logstash",
            "transport": "logstash_async.transport.TcpTransport",
            "host": LOGSTASH_HOST,
            "port": LOGSTASH_PORT,
            "ssl_enable": LOGSTASH_SSL_ENABLE,
            "database_path": f"{PROJECT_ROOT}/logstash.db",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": f"{PROJECT_ROOT}/{PROJECT_NAME}.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "kn_middleware_logger": {
            "handlers": ["logstash"],
            "level": "INFO",
        },
        "default": {
            "handlers": ["logstash"],
            "level": "DEBUG",
        },
        "kn_function_logger": {
            "handlers": ["logstash"],
            "level": "DEBUG",
        },
    },
}


def log(
    level, msg, collect_localvars=True, exc_info=None, extra=None, stack_info=False
):
    import inspect

    extra = extra or {}
    vars = {}
    caller_name = ""
    if collect_localvars:
        frame = inspect.currentframe()
        calframe = inspect.getouterframes(frame, 2)
        try:
            vars = frame.f_back.f_locals
            caller_name = calframe[1][3]

        finally:
            del frame

    extra["vars"] = vars
    extra["caller_name"] = vars

    logger.log(level, msg, exc_info=exc_info, extra=extra, stack_info=stack_info)


def logging_decorator(func, *, level=10, msg=""):
    @wraps(func)
    def function_wrapper(*args, **kwargs):
        logger = logging.getLogger("kn_function_logger")
        message = msg or func.__name__

        return_value = func(*args, **kwargs)
        logger.log(
            level,
            message,
            extra={
                "func_args": args,
                "func_kwargs": kwargs,
                "func_return_value": return_value,
            },
        )
        return return_value

    return function_wrapper


def get_base_logging(logstash=True):
    if logstash:
        return BASE_LOGGING
    _logging = copy.deepcopy(BASE_LOGGING)
    for logger in _logging["loggers"].keys():
        _logging["loggers"][logger]["handlers"] = [
            "file",
        ]
    return _logging
