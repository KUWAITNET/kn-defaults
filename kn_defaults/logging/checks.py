from django.conf import settings
from django.core.checks import Error, register


@register()
def check_logging_settings(app_configs=None, **kwargs):
    errors = []
    logging_dict = settings.LOGGING
    loggers = logging_dict.get('loggers', {})
    kn_logging = loggers.get('kn_defaults', False)
    if not kn_logging:
        errors.append(Error('`kn_defaults` is not added to LOGGING.loggers',
                            hint="add kn_defaults to LOGGING.loggers objects",
                            obj='settings',
                            id='kn_defaults.E001', ))
    return errors
