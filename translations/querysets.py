from django.db import models, transaction

from translations.utils import get_translations, translate, update_translations


class TranslatableQuerySet(models.QuerySet):

    def get_translations(self, *relations, lang=None):
        return get_translations(self, *relations, lang=lang)

    def get_translated(self, *relations, lang=None, translations_queryset=None):
        translate(
            self, *relations,
            lang=lang,
            translations_queryset=translations_queryset
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
