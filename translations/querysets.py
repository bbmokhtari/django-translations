from django.db import models, transaction

from translations.utils import apply_translations, update_translations


class TranslatableQuerySet(models.QuerySet):

    def get_translated(self, *relations, lang=None):
        apply_translations(
            self, *relations,
            lang=lang
        )
        return self

    def create_translated(self, lang=None, **kwargs):
        try:
            with transaction.atomic():
                instance = self.create(**kwargs)
                update_translations(instance, lang=lang)
                return instance
        except Exception:
            raise
