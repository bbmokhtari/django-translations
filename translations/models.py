"""
This module contains the models for the Translations app.

.. rubric:: Classes:

:class:`Translatable`
    An abstract model which must be inherited by the
    models needing translation capabilities.
:class:`Translation`
    The model which represents the translations.

----
"""

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, \
    GenericRelation
from django.utils.translation import ugettext_lazy as _

from translations.utils import get_translations, translate, update_translations
from translations.managers import TranslatableManager


__docformat__ = 'restructuredtext'


class Translation(models.Model):
    """
    This model represents the translations.

    Each translation belongs to a unique database address. Each address is
    combined of a `content_type` (model), `object_id` (row) and a `field`
    (column).

    Each unique address must have only one translation in a specific
    `language`.
    """
    content_type = models.ForeignKey(
        verbose_name=_('content type'),
        help_text=_('the content type of the object to translate'),
        to=ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.TextField(
        verbose_name=_('object id'),
        help_text=_('the id of the object to translate')
    )
    content_object = GenericForeignKey(
        ct_field='content_type',
        fk_field='object_id'
    )
    field = models.CharField(
        verbose_name=_('field'),
        help_text=_('the field of the object to translate'),
        max_length=64
    )
    language = models.CharField(
        verbose_name=_('language'),
        help_text=_('the language of the translation'),
        max_length=32,
        choices=settings.LANGUAGES
    )
    text = models.TextField(
        verbose_name=_('text'),
        help_text=_('the text of the translation')
    )

    def __str__(self):
        """Return the representation of the translation."""
        return '{source}: {translation}'.format(
            source=getattr(self.content_object, self.field),
            translation=self.text
        )

    class Meta:
        unique_together = ('content_type', 'object_id', 'field', 'language',)
        verbose_name = _('translation')
        verbose_name_plural = _('translations')


class Translatable(models.Model):
    """
    This abstract model can be inherited by another model to make it
    translatable.

    Inheriting this abstract model adds `translations` relation and changes the
    `objects` manager to add translation capabilities to the ORM.
    """

    objects = TranslatableManager()
    translations = GenericRelation(
        Translation,
        content_type_field='content_type',
        object_id_field='object_id',
        related_query_name="%(app_label)s_%(class)s"
    )

    class Meta:
        abstract = True

    class TranslatableMeta:
        """
        This class contains meta information about translation process.

        This includes setting the `fields` attribute. which specifies which
        fields the user wants translated. If this attribute is not set the
        fields will be determined automatically.
        """
        # the reason to chose None over an empty list ([]) is that the user
        # might want to set `fields` explicitly to an empty list.
        fields = None

    @classmethod
    def get_translatable_fields(cls):
        """
        Return a list of translatable fields.

        Do this either using the `TranslatableMeta`.`fields` property or do
        this automatically.
        """
        if hasattr(cls, 'TranslatableMeta'):
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
        else:
            raise Exception(
                '{cls} class is not a translatable model.'.format(cls=cls)
            )
        return fields

    def update_translations(self, lang=None):
        """
        Update the translations of the object based on the language code.
        """
        update_translations(self, lang=lang)

    def get_translations(self, *relations, lang=None):
        """
        Return the translations of the object and its relations based on the
        language code.
        """
        return get_translations(self, *relations, lang=lang)

    def get_translated(self, *relations, lang=None, translations=None):
        """
        Return the translated object and its relations based on the language
        code.

        Optionally a `translations` queryset can be passed as well, if it is
        not passed it will be queried automatically.
        """
        translate(
            self, *relations,
            lang=lang,
            translations_queryset=translations
        )
        return self
