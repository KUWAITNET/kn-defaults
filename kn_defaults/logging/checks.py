from django.conf import settings
from django.core.checks import Error, register, Warning
from django.urls import reverse, NoReverseMatch


@register()
def check_logging_settings(app_configs=None, **kwargs):
    errors = []
    if settings.LOGGING_CONFIG is None:
        errors.append(Warning('LOGGING_CONFIG is set to None which disable logging all together !!'))

    logging_dict = settings.LOGGING
    loggers = logging_dict.get('loggers', {})
    kn_logging = loggers.get('kn_middleware_logger', False)
    if not kn_logging:
        errors.append(Error('`kn_defaults` is not added to LOGGING.loggers',
                            hint="add kn_defaults to LOGGING.loggers objects",
                            obj='settings',
                            id='kn_defaults.E001', ))
    return errors


@register()
def check_raven(app_configs, **kwargs):
    errors = []
    if 'raven.contrib.django.raven_compat' not in settings.INSTALLED_APPS and not settings.DEBUG:
        errors.append(
            Error('`raven.contrib.django.raven_compat` is missing from INSTALLED_APPS',
                  obj='settings',
                  id='kn_defaults.E002',
                  )
        )

    raven_config = getattr(settings, 'RAVEN_CONFIG', {})
    if not raven_config:
        errors.append(
            Error('`RAVEN_CONFIG` is missing from settings',
                  hint='Add `RAVEN_CONFIG={"dsn":"<DSN HERE>"}` to relevant settings file',
                  obj='settings',
                  id='kn_defaults.E003',
                  )
        )

    return errors


@register()
def check_admin_url(app_configs, **kwargs):
    errors = []
    try:
        admin_url = reverse('admin:index')
    except NoReverseMatch:
        # no default admin in url, exiting
        return errors

    error_class = Warning if settings.DEBUG else Error
    url_parts = admin_url.split('/')
    if 'admin' in url_parts:
        errors.append(
            error_class(
                "it’s not recommended to have the admin url as `/admin/` and it will not work when DEBUG = False. "
                "Please change it to a different url or ask your project manager what url should be used.",
                hint='Change the admin url',
                obj='settings',
                id='kn_defaults.E003')
        )
    return errors
