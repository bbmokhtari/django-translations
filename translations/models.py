"""
This module contains the models for the Translations app. It contains the
following members:

:class:`Translation`
    The model which represents the translations.
:class:`Translatable`
    An abstract model which provides custom translation functionalities.
"""

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, \
    GenericRelation
from django.utils.translation import ugettext_lazy as _

__docformat__ = 'restructuredtext'


class Translation(models.Model):
    """
    The model which represents the translations.

    Each translation belongs to a *unique* database address. Each address is
    composed of a :attr:`content_type` (table), an :attr:`object_id` (row) and
    a :attr:`field` (column). Each unique address must have only one
    translation :attr:`text` in a specific :attr:`language`.

    .. note::

       :attr:`content_type` and :attr:`object_id` together form something
       called a :class:`~django.contrib.contenttypes.fields.GenericForeignKey`.
       This kind of foreign key contrary to the normal foreign key (which can
       point to a row in only one table) can point to a row in any table.

    .. note::

       :attr:`object_id` is defined as a :class:`~django.db.models.CharField`
       so that it can also point to the rows in the tables which use character
       fields (like :class:`~django.db.models.UUIDField`, etc.) as primary key.

    .. warning::

       Try **not** to work with the :class:`~translations.models.Translation`
       model directly unless you *really* have to and you know what you're
       doing.

       Instead use the functionalities provided in
       the :class:`~translations.models.Translatable` model.

    To create the translation of a field manually:

    .. testsetup:: Translation

       from tests.sample import create_samples

       create_samples(
           continent_names=['europe'],
       )

    .. testcode:: Translation

       from django.contrib.contenttypes.models import ContentType
       from sample.models import Continent
       from translations.models import Translation

       europe = Continent.objects.get(code='EU')

       translation = Translation.objects.create(
           content_type=ContentType.objects.get_for_model(Continent),
           object_id=europe.id,
           field='name',
           language='de',
           text='Europa',
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
            translation=self.text,
        )

    class Meta:
        unique_together = ('content_type', 'object_id', 'field', 'language',)
        verbose_name = _('translation')
        verbose_name_plural = _('translations')


class Translatable(models.Model):
    """
    An abstract model which provides custom translation functionalities.

    Provides functionalities like :meth:`apply_translations` to read the
    translations from the database and apply them on an instance, and
    :meth:`update_translations` to update the translations from an instance
    and write them on the database.

    It changes the default manager of the model to
    :class:`~translations.querysets.TranslatableQuerySet` in order to provide
    custom translation functionalities in the querysets.

    It also adds the :attr:`translations` relation to the model, just in case
    any one wants to work with the translations of an instance manually.

    .. note::

       The :attr:`translations` relation is the reverse relation of the
       :class:`~django.contrib.contenttypes.fields.GenericForeignKey`
       described in :class:`~translations.models.Translation`. It's a
       :class:`~django.contrib.contenttypes.fields.GenericRelation`.
    """

    translations = GenericRelation(
        Translation,
        content_type_field='content_type',
        object_id_field='object_id',
        related_query_name='%(app_label)s_%(class)s',
    )

    class Meta:
        abstract = True

    @classmethod
    def get_translatable_fields(cls):
        """
        Return the translatable fields of the model.

        Returns the translatable fields of the model based on the
        field names listed in :attr:`TranslatableMeta.fields`.

        :return: The translatable fields of the model.
        :rtype: list(~django.db.models.Field)

        Considering this model:

        .. literalinclude:: ../../sample/models.py
           :pyobject: Continent
           :emphasize-lines: 27-28

        To get the translatable fields of the mentioned model:

        .. testcode:: get_translatable_fields

           from sample.models import Continent

           for field in Continent.get_translatable_fields():
               print(field)

        .. testoutput:: get_translatable_fields

           sample.Continent.name
           sample.Continent.denonym
        """
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
        """
        Return the names of the model's translatable fields.

        Returns the names of the model's translatable fields based on the
        field names listed in :attr:`TranslatableMeta.fields`.

        :return: The names of the model's translatable fields.
        :rtype: list(str)

        Considering this model:

        .. literalinclude:: ../../sample/models.py
           :pyobject: Continent
           :emphasize-lines: 27-28

        To get the names of the mentioned model's translatable fields:

        .. testcode:: _get_translatable_fields_names

           from sample.models import Continent

           for name in Continent._get_translatable_fields_names():
               print(name)

        .. testoutput:: _get_translatable_fields_names

           name
           denonym
        """
        if not hasattr(cls, '_cached_translatable_fields_names'):
            cls._cached_translatable_fields_names = [
                field.name for field in cls.get_translatable_fields()
            ]
        return cls._cached_translatable_fields_names

    @classmethod
    def _get_translatable_fields_choices(cls):
        """
        Return the choices of the model's translatable fields.

        Returns the choices of the model's translatable fields based on the
        field names listed in :attr:`TranslatableMeta.fields`.

        :return: The choices of the model's translatable fields.
        :rtype: list(tuple(str, str))

        Considering this model:

        .. literalinclude:: ../../sample/models.py
           :pyobject: Continent
           :emphasize-lines: 27-28

        To get the choices of the mentioned model's translatable fields:

        .. testcode:: _get_translatable_fields_choices

           from sample.models import Continent

           for choice in Continent._get_translatable_fields_choices():
               print(choice)

        .. testoutput:: _get_translatable_fields_choices

           (None, '---------')
           ('name', 'name')
           ('denonym', 'denonym')
        """
        choices = [
            (None, '---------'),
        ]

        for field in cls.get_translatable_fields():
            choice = (field.name, field.verbose_name)
            choices.append(choice)

        return choices

    class TranslatableMeta:
        """
        The class which contains meta information about the translation
        of the model instances.
        """

        fields = None
        """
        :var fields: The names of the fields to use in the translation.
            ``None`` means use the text based fields automatically.
            ``[]`` means use no fields.
        :vartype fields: list(str) or None
        """
