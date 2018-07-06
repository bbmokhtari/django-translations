from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TranslationsConfig(AppConfig):
    name = 'translations'
    verbose_name = _('translations')
