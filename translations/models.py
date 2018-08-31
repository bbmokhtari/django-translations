"""
This module contains the models for the Translations app. It contains the
following members:

:class:`Translation`
    The model which represents the translations.
:class:`Translatable`
    An abstract model which can be inherited by any model that needs
    translation capabilities.
"""

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, \
    GenericRelation
from django.utils.translation import ugettext_lazy as _

from translations.utils import apply_translations, update_translations
from translations.querysets import TranslatableQuerySet


__docformat__ = 'restructuredtext'


class Translation(models.Model):
    """
    The model which represents the translations.

    Manages storing, querying and the structure of the translation objects.

    Each translation belongs to a *unique* database address. Each address is
    composed of a :attr:`content_type` (table), an :attr:`object_id` (row) and
    a :attr:`field` (column).

    Each unique address must have only one translation in a specific
    :attr:`language`.

    .. note::

       :class:`~django.contrib.contenttypes.models.ContentType` is a django
       model which comes with the :mod:`~django.contrib.contenttypes` app.
       It represents the tables created in a database by all the apps in a
       project.

       :attr:`content_type` and :attr:`object_id` together form something
       called a :class:`~django.contrib.contenttypes.fields.GenericForeignKey`.
       This kind of foreign key contrary to the normal foreign key (which can
       point to a row in only one table) can point to a row in any table.

    .. warning::

       Try **not** to work with the :class:`~translations.models.Translation`
       model manually unless you *really* have to and you know what you're
       doing.

       Instead use the functionalities provided in
       the :class:`~translations.models.Translatable` model.

    To create the translation of a field manually:

    .. testsetup:: Translation

       from tests.sample import create_samples

       create_samples(
           continent_names=["europe"],
       )

    .. testcode:: Translation

       from django.contrib.contenttypes.models import ContentType
       from sample.models import Continent
       from translations.models import Translation

       europe = Continent.objects.get(code='EU')

       content_type = ContentType.objects.get_for_model(europe)

       translation = Translation.objects.create(
           content_type=content_type,
           object_id=europe.id,
           field='name',
           language='de',
           text='Europa'
       )

       print(translation)

    .. testoutput:: Translation

       Europe: Europa
    """

    objects = models.Manager()

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
            translation=self.text
        )

    class Meta:
        unique_together = ('content_type', 'object_id', 'field', 'language',)
        verbose_name = _('translation')
        verbose_name_plural = _('translations')


class Translatable(models.Model):
    """
    An abstract model which provides custom translation functionalities.

    Provides functionalities like :meth:`apply_translations` to read and apply
    translations from the database onto the instance, and
    :meth:`update_translations` to write and update translations from the
    instance onto the database.

    It changes the default manager of the model to
    :class:`~translations.querysets.TranslatableQuerySet` in order to provide
    custom translation functionalities in the querysets.

    It also adds the :attr:`translations` relation to the model, just in case
    any one wants to work with the translations of the instances manually.

    .. note::

       The :attr:`translations` relation is the reverse relation of the
       :class:`~django.contrib.contenttypes.fields.GenericForeignKey`
       described in :class:`Translation`. It's a
       :class:`~django.contrib.contenttypes.fields.GenericRelation`.
    """

    objects = TranslatableQuerySet.as_manager()
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
        The class which contains meta information about the translation
        process.
        """

        fields = None
        """
        :var fields: The names of the fields to use in the translation
            process.
            ``None`` means use the text based fields automatically.
            ``[]`` means use no fields.
        :vartype fields: list(str) or None
        """

    @classmethod
    def get_translatable_fields(cls):
        """
        Return the translatable fields of the model.

        Returns the translatable fields of the model based on the field names
        listed in :attr:`TranslatableMeta.fields`.

        :return: The translatable fields.
        :rtype: list(~django.db.models.Field)
        """
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
                            hasattr(field, 'choices')
                        ):
                    fields.append(field)
        else:
            fields = [
                cls._meta.get_field(field_name)
                for field_name in cls.TranslatableMeta.fields
            ]
        return fields

    def apply_translations(self, *relations, lang=None):
        r"""
        Translate the object and its relations (in place) in a language.

        Translate the current object and its relations in a language
        based on a queryset of translations and return it. If no
        ``translations`` queryset is given one will be created based on the
        ``relations`` and the ``lang`` parameters.

        .. note::
           It's recommended that the ``translations`` queryset is not passed
           in, so it's calculated automatically. Translations app is pretty
           smart, it will fetch all the translations for the object and its
           relations doing the minimum amount of queries needed (usually one).
           It's only there just in case there is a need to query the
           translations manually.

        :param \*relations: a list of relations to translate
        :type \*relations: list(str)
        :param lang: the language of the translation, if ``None``
            is given the current active language will be used.
        :type lang: str or None
        """
        apply_translations(self, *relations, lang=lang)

    def update_translations(self, *relations, lang=None):
        """
        Update the translations of the object based on the object properties.

        Use the current properties of the object to update the translations in
        a language.

        :param lang: the language of the translations to update, if ``None``
            is given the current active language will be used.
        :type lang: str or None
        """
        update_translations(self, *relations, lang=lang)
