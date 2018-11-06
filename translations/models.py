"""This module contains the models for the Translations app."""

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, \
    GenericRelation
from django.utils.translation import ugettext_lazy as _

from translations.querysets import TranslatableQuerySet


__docformat__ = 'restructuredtext'


class Translation(models.Model):
    """The model which represents the translations."""

    content_type = models.ForeignKey(
        verbose_name=_('content type'),
        help_text=_('the content type of the object to translate'),
        to=ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.CharField(
        verbose_name=_('object id'),
        help_text=_('the id of the object to translate'),
        max_length=128,
    )
    content_object = GenericForeignKey(
        ct_field='content_type',
        fk_field='object_id',
    )
    field = models.CharField(
        verbose_name=_('field'),
        help_text=_('the field of the object to translate'),
        max_length=64,
    )
    language = models.CharField(
        verbose_name=_('language'),
        help_text=_('the language of the translation'),
        max_length=32,
        choices=settings.LANGUAGES,
    )
    text = models.TextField(
        verbose_name=_('text'),
        help_text=_('the text of the translation'),
    )

    def __str__(self):
        """Return the representation of the translation."""
        return '{source}: {translation}'.format(
            source=getattr(self.content_object, self.field),
            translation=self.text,
        )

    class Meta:
        unique_together = ('content_type', 'object_id', 'field', 'language',)
        verbose_name = _('translation')
        verbose_name_plural = _('translations')


class Translatable(models.Model):
    """An abstract model which provides custom translation functionalities."""
    objects = TranslatableQuerySet.as_manager()
    translations = GenericRelation(
        Translation,
        content_type_field='content_type',
        object_id_field='object_id',
        related_query_name='%(app_label)s_%(class)s',
    )

    class Meta:
        abstract = True

    class TranslatableMeta:
        """
        This class contains meta information about the translation
        of the model instances.
        """

        fields = None

    @classmethod
    def get_translatable_fields(cls):
        """Return the model’s translatable fields."""
        if not hasattr(cls, '_cached_translatable_fields'):
            if cls.TranslatableMeta.fields is None:
                fields = []
                for field in cls._meta.get_fields():
                    if isinstance(
                                field,
                                (models.CharField, models.TextField,)
                            ) and not isinstance(
                                field,
                                models.EmailField
                            ) and not (
                                hasattr(field, 'choices') and field.choices
                            ):
                        fields.append(field)
            else:
                fields = [
                    cls._meta.get_field(field_name)
                    for field_name in cls.TranslatableMeta.fields
                ]
            cls._cached_translatable_fields = fields
        return cls._cached_translatable_fields

    @classmethod
    def _get_translatable_fields_names(cls):
        """Return the names of the model's translatable fields."""
        if not hasattr(cls, '_cached_translatable_fields_names'):
            cls._cached_translatable_fields_names = [
                field.name for field in cls.get_translatable_fields()
            ]
        return cls._cached_translatable_fields_names

    @classmethod
    def _get_translatable_fields_choices(cls):
        """Return the choices of the model's translatable fields."""
        choices = [
            (None, '---------'),
        ]

        for field in cls.get_translatable_fields():
            choice = (field.name, field.verbose_name.title())
            choices.append(choice)

        return choices
