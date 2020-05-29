import logging
import os

logger = logging.getLogger('default')

KN_FORMATTER = "%(levelname)s:%(name)s; " \
               "REQ_id:%(request_id)s; %(message)s; path=%(path)s; method=%(method)s;ip=%(ip)s; " \
               "status_code:%(status_code)%; response_duration:%(response_duration)s; " \
               "post_parameters: %(post_parameters)s; outbound:%(outbound_payload)s"

BASE_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose_kn': {
            'format': KN_FORMATTER,
        },
        'verbose_project': {
            'format': '{levelname}:{message} - LocalVars={vars} ',
            'style': '{',

        }
    },
    'handlers': {
        'kn_default_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose_project'
        },
        'file_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.getcwd(), 'log.log'),
            'maxBytes': 1024 * 1024,
            'backupCount': 3,
            'formatter': 'verbose_project',
        },
    },
    'loggers': {
        'kn_defaults': {
            'handlers': ['kn_default_handler'],
            'level': 'INFO',
        },
        'default': {
            'handlers': ['file_log'],
            'level': 'DEBUG',
        }
    }
}


def log(level, msg, exc_info=None, extra=None, stack_info=False):
    import inspect
    extra = extra or {}
    vars = {}
    frame = inspect.currentframe()
    try:
        vars = frame.f_back.f_locals
    finally:
        del frame
    extra['vars'] = vars

    logger.log(level, msg, exc_info=exc_info, extra=extra, stack_info=stack_info)
