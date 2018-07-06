from django.db import models

from .querysets import TranslatableQuerySet


class TranslatableManager(models.Manager):

    def get_queryset(self):
        return TranslatableQuerySet(self.model, using=self._db)

    def get_translations(self, *relations, iso_alpha_2_language_code=None):
        return self.get_queryset().get_translations(
            *relations,
            iso_alpha_2_language_code=iso_alpha_2_language_code
        )

    def get_translated(self,
                       *relations,
                       iso_alpha_2_language_code=None,
                       translations_queryset=None):
        return self.get_queryset().get_translated(
            *relations,
            iso_alpha_2_language_code=iso_alpha_2_language_code,
            translations_queryset=translations_queryset
        )

    def create_translated(self, iso_alpha_2_language_code=None, **kwargs):
        field = getattr(self, 'field', None)
        field = field.name if field else None
        instance = getattr(self, 'instance', None)

        if field and instance and field not in kwargs:
            kwargs[field] = instance

        return self.get_queryset().create_translated(iso_alpha_2_language_code=iso_alpha_2_language_code, **kwargs)
