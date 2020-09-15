from django.conf import settings
from django.core.checks import Error, register, Warning
from django.urls import reverse, NoReverseMatch

from . import app_settings
import environ

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


# @register()
def check_raven(app_configs, **kwargs):
    errors = []
    env = environ.Env()
    sentry_dsn = env.str("SENTRY_DSN", "")

    if not sentry_dsn and not settings.DEBUG:
        errors.append(
            Error('`SENTRY_DSN is not in the environment variables',
                  obj='settings',
                  id='kn_defaults.E002',
                  )
        )
    #
    # raven_config = getattr(settings, 'RAVEN_CONFIG', {})
    # if not raven_config:
    #     errors.append(
    #         Error('`RAVEN_CONFIG` is missing from settings',
    #               hint='Add `RAVEN_CONFIG={"dsn":"<DSN HERE>"}` to relevant settings file',
    #               obj='settings',
    #               id='kn_defaults.E003',
    #               )
    #     )

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


@register()
def check_apm(app_configs, **kwargs):
    errors = []
    # INSTALLATION_NAME = env.list('DJANGO_ALLOWED_HOSTS')[0].replace('.', '-')
    if app_settings.KN_PRODUCTION:
        # check that APM is enabled
        if not getattr(settings, 'ENABLE_APM', False):
            errors.append(Warning('APM is not enabled for this project !!'))
        else:
            if 'elasticapm.contrib.django' not in settings.INSTALLED_APPS:
                errors.append(Error('Please Add APM TO INSTALLED APPS',
                                    hint="INSTALLED_APPS.append('elasticapm.contrib.django')"))
            if 'elasticapm.contrib.django.middleware.TracingMiddleware' not in settings.MIDDLEWARE:
                errors.append(Error('Please Add APM TO MIDDLEWARE',
                                    hint='MIDDLEWARE.insert(0, "elasticapm.contrib.django.middleware.TracingMiddleware")'))
            ELASTIC_APM = getattr(settings, 'ELASTIC_APM', False)
            if not ELASTIC_APM:
                errors.append(Error('Please Add ELASTIC_APM TO your settings file',
                                    hint="""ELASTIC_APM = {
    "SERVICE_NAME": INSTALLATION_NAME,
    "SERVER_URL": "<YOUR_UP:PORT>",
    "DJANGO_TRANSACTION_NAME_FROM_ROUTE": True,
}"""))


            if not getattr(settings, 'INSTALLATION_NAME', False):
                errors.append(Error('Please Add an APM installation name',
                                    hint="INSTALLATION_NAME = env.list('DJANGO_ALLOWED_HOSTS')[0].replace('.', '-')"))
    return errors
