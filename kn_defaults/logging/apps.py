from django import apps

from django.conf import settings


class KnDefault(apps.AppConfig):
    name = 'kn_defaults.logging'
    verbose_name = 'KuwaitNet Helpers'

    def ready(self):
        super().ready()
        from .app_settings import DISABLE_CMS_PLUGIN_CHANGE_ADMIN_LOG
        from . import checks
        if 'cms' in settings.INSTALLED_APPS and not DISABLE_CMS_PLUGIN_CHANGE_ADMIN_LOG:
            from .handlers import cms_plugin_change_admin_log
            from cms.signals import post_placeholder_operation
            post_placeholder_operation.connect(cms_plugin_change_admin_log)
