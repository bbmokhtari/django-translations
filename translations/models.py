"""
This module contains the models for the Translations app.

.. rubric:: Classes:

:class:`Translatable`
    An abstract model which can be inherited by any model that needs
    translation capabilities.
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

from translations.utils import apply_translations, update_translations
from translations.managers import TranslatableManager


__docformat__ = 'restructuredtext'


class Translation(models.Model):
    """
    This model represents the translations.

    Each translation belongs to a *unique* database address. Each address is
    composed of a :attr:`content_type` (table), an :attr:`object_id` (row) and
    a :attr:`field` (column).

    Each unique address must have only one translation in a specific
    :attr:`language`.

    .. note::

       :class:`~django.contrib.contenttypes.models.ContentType` is a django
       model which comes with the :mod:`~django.contrib.contenttypes` app.
       This model represents the tables created in the database.

       :attr:`content_type` and :attr:`object_id` together form something
       called a :class:`~django.contrib.contenttypes.fields.GenericForeignKey`.
       This kind of foreign key contrary to the normal foreign key (which can
       point to a row in only one table) can point to a row in any table.

    .. warning:: Never work with the :class:`Translation` model directly
       unless you really have to. (it's unlikely it ever happens)

       Working directly with the :class:`Translation` model is discouraged
       because it leads to hard, error prone and inefficient code. so never
       do this. Here's an example why.

    .. commented doctest
       first create an object:

       >>> from polls.models import Question
       >>> from django.utils import timezone
       >>> question = Question.objects.create(
       ...     question_text='How old are you?',
       ...     pub_date=timezone.now()
       ... )

       now let's create a translation for it manually:

       >>> # hard: look at the amount of effort to do this
       >>> # error prone: note the `field` is set manually
       >>> # inefficient: consider the creation of multiple translations
       >>> from django.contrib.contenttypes.models import ContentType
       >>> from translations.models import Translation
       >>> question_ct = ContentType.objects.get_for_model(Question)
       >>> Translation.objects.create(
       ...     content_type=question_ct,
       ...     object_id=question.id,
       ...     field='question_text',
       ...     language='fr',
       ...     text='Quel âge avez-vous?'
       ... )
       <Translation: How old are you?: Quel âge avez-vous?>

       The same can also be achieved with this.

       >>> # hard, error prone and inefficient AGAIN
       >>> from translations.models import Translation
       >>> Translation.objects.create(
       ...     content_object=question,
       ...     field='question_text',
       ...     language='fr',
       ...     text='Quel âge avez-vous?'
       ... )
       <Translation: How old are you?: Quel âge avez-vous?>

       Never do this! This is just for the sake of demonstration.

       The correct way to do this, is to use the :class:`Translatable` model.

       >>> # the easy, correct and efficient way
       >>> # inherit `Question` model from `Translatable`
       >>> question.question_text = 'Quel âge avez-vous?'
       >>> question.update_translations(lang='fr')
       <Question: Quel âge avez-vous?>
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
    This abstract model can be inherited by any model which needs translation
    capabilities.

    Inheriting this model adds :attr:`translations` relation to the model and
    changes the :attr:`objects` manager of the model to add translation
    capabilities to the ORM.

    .. note::
       There is **no need for migrations** after inheriting this model. Simply
       just use it afterwards!

    .. note::
       The :attr:`translations` relation is a reverse relation to the
       :class:`~django.contrib.contenttypes.fields.GenericForeignKey`
       described in :class:`Translation`.
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
        """This class contains meta information about translation process."""

        fields = None
        """
        :var fields: The fields of the model to be translated, ``None`` means
            use all text based fields automatically, ``[]`` means no fields
            should be translatable.
        :vartype fields: list(str) or None
        """

    @classmethod
    def get_translatable_fields(cls):
        """
        Return the list of translatable fields.

        Return the translatable fields for the model based on
        :attr:`TranslatableMeta.fields`.

        :return: The list of translatable fields
        :rtype: list(~django.db.models.Field)
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
