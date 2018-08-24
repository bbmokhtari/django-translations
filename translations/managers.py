from django.db import models

from .querysets import TranslatableQuerySet


class TranslatableManager(models.Manager):

    def get_queryset(self):
        return TranslatableQuerySet(self.model, using=self._db)

    def get_translated(self,
                       *relations,
                       lang=None):
        return self.get_queryset().get_translated(
            *relations,
            lang=lang
        )

    def create_translated(self, lang=None, **kwargs):
        field = getattr(self, 'field', None)
        field = field.name if field else None
        instance = getattr(self, 'instance', None)

        if field and instance and field not in kwargs:
            kwargs[field] = instance

        return self.get_queryset().create_translated(lang=lang, **kwargs)
