from django import apps


class KnDefault(apps.AppConfig):
    name = 'kn_defaults.logging'
    verbose_name = 'KuwaitNet Helpers'

    def ready(self):
        super().ready()
        # todo call checks



