from django.db import models, transaction

from translations.utils import get_translations, translate, update_translations


class TranslatableQuerySet(models.QuerySet):

    def get_translations(self, *relations, iso_alpha_2_language_code=None):
        return get_translations(self, *relations, iso_alpha_2_language_code=iso_alpha_2_language_code)

    def get_translated(self, *relations, iso_alpha_2_language_code=None, translations_queryset=None):
        translate(
            self, *relations,
            iso_alpha_2_language_code=iso_alpha_2_language_code,
            translations_queryset=translations_queryset
        )
        return self

    def create_translated(self, iso_alpha_2_language_code=None, **kwargs):
        try:
            with transaction.atomic():
                instance = self.create(**kwargs)
                update_translations(instance, iso_alpha_2_language_code=iso_alpha_2_language_code)
                return instance
        except Exception:
            raise
