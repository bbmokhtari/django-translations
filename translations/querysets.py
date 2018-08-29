from django.db import models, transaction

from translations.utils import apply_translations, update_translations


class TranslatableQuerySet(models.QuerySet):

    def apply_translations(self, *relations, lang=None):
        apply_translations(self, *relations, lang=lang)
        return self

    def update_translations(self, *relations, lang=None):
        update_translations(self, *relations, lang=lang)
        return self
