from django.apps import AppConfig
try:
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    from django.utils.translation import gettext_lazy as _


class TranslationsConfig(AppConfig):
    name = 'translations'
    verbose_name = _('translations')
