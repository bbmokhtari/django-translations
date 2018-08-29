from django.db import models

from .querysets import TranslatableQuerySet


class TranslatableManager(models.Manager):

    def get_queryset(self):
        return TranslatableQuerySet(self.model, using=self._db)

    def apply_translations(self, *relations, lang=None):
        return self.get_queryset().apply_translations(*relations, lang=lang)

    def update_translations(self, lang=None):
        return self.get_queryset().update_translations(lang=lang)
