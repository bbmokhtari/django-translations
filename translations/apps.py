from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TranslationsConfig(AppConfig):
    name = 'translations'
    verbose_name = _('translations')

    def ready(self):
        try:
            # cache all content types at the start
            from django.contrib.contenttypes.models import ContentType
            models = [ct.model_class() for ct in ContentType.objects.all()]
            ContentType.objects.get_for_models(*models)
        except Exception:
            pass
