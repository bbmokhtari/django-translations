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

from .utils import apply_translations, update_translations
from .querysets import TranslatableQuerySet


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

    objects = TranslatableQuerySet.as_manager()

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
        if not hasattr(cls, '_cached_translatable_fields_choices'):
            choices = [
                (None, '---------'),
            ]
            for field in cls.get_translatable_fields():
                choice = (field.name, field.verbose_name)
                choices.append(choice)
            cls._cached_translatable_fields_choices = choices
        return cls._cached_translatable_fields_choices

    def apply_translations(self, *relations, lang=None):
        """
        Apply the translations of the instance and some relations of it in a
        language.

        Fetches the translations of the instance and the specified relations
        of it in a language and applies them on the translatable
        :attr:`~translations.models.Translatable.TranslatableMeta.fields` of
        the instance and the relations of it in place.

        :param relations: The relations of the instance to apply the
            translations of.
        :type relations: list(str)
        :param lang: The language to fetch the translations in.
            ``None`` means use the :term:`active language` code.
        :type lang: str or None
        :raise TypeError: If the models of the included relations are
            not :class:`~translations.models.Translatable`.
        :raise ~django.core.exceptions.FieldDoesNotExist: If a relation is
            pointing to the fields that don't exist.
        :raise ValueError: If the language code is not included in
            the :data:`~django.conf.settings.LANGUAGES` setting.

        .. testsetup:: apply_translations

           from tests.sample import create_samples

           create_samples(
               continent_names=['europe', 'asia'],
               country_names=['germany', 'south korea'],
               city_names=['cologne', 'munich', 'seoul', 'ulsan'],
               continent_fields=['name', 'denonym'],
               country_fields=['name', 'denonym'],
               city_fields=['name', 'denonym'],
               langs=['de']
           )

        .. note::

           If there is no translation for a field in translatable
           :attr:`~translations.models.Translatable.TranslatableMeta.fields`,
           the translation of the field falls back to the value of the field
           in the instance.

        .. note::

           It is **recommended** for the relations of the instance to be
           prefetched before applying the translations in order to reach
           optimal performance.

           To do this use
           :meth:`~django.db.models.query.QuerySet.select_related`,
           :meth:`~django.db.models.query.QuerySet.prefetch_related` or
           :func:`~django.db.models.prefetch_related_objects`.

        To apply the translations of an instance and the relations of it:

        .. testcode:: apply_translations

           from sample.models import Continent

           relations = ('countries', 'countries__cities',)

           europe = Continent.objects.prefetch_related(
               *relations,
           ).get(code='EU')

           europe.apply_translations(
               *relations,
               lang='de',
           )

           print('Continent: {}'.format(europe))
           for country in europe.countries.all():
               print('Country: {}'.format(country))
               for city in country.cities.all():
                   print('City: {}'.format(city))

        .. testoutput:: apply_translations

           Continent: Europa
           Country: Deutschland
           City: Köln
           City: München

        .. warning::

           Filtering any queryset after applying the translations will cause
           the translations of that queryset to be reset.

           .. testcode:: apply_translations

              from sample.models import Continent

              relations = ('countries', 'countries__cities',)

              europe = Continent.objects.prefetch_related(
                  *relations,
              ).get(code='EU')

              europe.apply_translations(
                  *relations,
                  lang='de',
              )

              print('Continent: {}'.format(europe))
              for country in europe.countries.exclude(name=''):  # Wrong
                  print('Country: {}  -- Wrong'.format(country))
                  for city in country.cities.all():
                      print('City: {}  -- Wrong'.format(city))

           .. testoutput:: apply_translations

              Continent: Europa
              Country: Germany  -- Wrong
              City: Cologne  -- Wrong
              City: Munich  -- Wrong

           The solution is to do the filtering before applying the
           translations. To do this on the relations use
           :class:`~django.db.models.Prefetch`.

           .. testcode:: apply_translations

              from django.db.models import Prefetch
              from sample.models import Continent, Country

              relations = ('countries', 'countries__cities',)

              europe = Continent.objects.prefetch_related(
                  Prefetch(
                      'countries',
                      queryset=Country.objects.exclude(name=''),  # Correct
                  ),
                  'countries__cities',
              ).get(code='EU')

              europe.apply_translations(
                  *relations,
                  lang='de',
              )

              print('Continent: {}'.format(europe))
              for country in europe.countries.all():
                  print('Country: {}'.format(country))
                  for city in country.cities.all():
                      print('City: {}'.format(city))

           .. testoutput:: apply_translations

              Continent: Europa
              Country: Deutschland
              City: Köln
              City: München
        """
        apply_translations(self, *relations, lang=lang)

    def update_translations(self, *relations, lang=None):
        """
        Update the translations of the instance and some relations of it in a
        language.

        Deletes the old translations of the instance and the specified
        relations of it in a language and creates new translations out of the
        translatable
        :attr:`~translations.models.Translatable.TranslatableMeta.fields` of
        the instance and the relations of it.

        :param relations: The relations of the instance to update the
            translations of.
        :type relations: list(str)
        :param lang: The language to update the translations in.
            ``None`` means use the :term:`active language` code.
        :type lang: str or None
        :raise TypeError: If the models of the included relations
            are not :class:`~translations.models.Translatable`.
        :raise ~django.core.exceptions.FieldDoesNotExist: If a relation is
            pointing to the fields that don't exist.
        :raise ValueError: If the language code is not included in
            the :data:`~django.conf.settings.LANGUAGES` setting.
        :raise RuntimeError: If any of the relations is not prefetched.

        .. testsetup:: update_translations_0

           from tests.sample import create_samples

           create_samples(
               continent_names=['europe', 'asia'],
               country_names=['germany', 'south korea'],
               city_names=['cologne', 'munich', 'seoul', 'ulsan'],
               continent_fields=['name', 'denonym'],
               country_fields=['name', 'denonym'],
               city_fields=['name', 'denonym'],
               langs=['de']
           )

        .. testsetup:: update_translations_1

           from tests.sample import create_samples

           create_samples(
               continent_names=['europe', 'asia'],
               country_names=['germany', 'south korea'],
               city_names=['cologne', 'munich', 'seoul', 'ulsan'],
               continent_fields=['name', 'denonym'],
               country_fields=['name', 'denonym'],
               city_fields=['name', 'denonym'],
               langs=['de']
           )

        .. note::

           It is **mandatory** for the relations of the instance to be
           prefetched before making any changes to them so that the changes
           can be fetched later.

           To do this use
           :meth:`~django.db.models.query.QuerySet.select_related`,
           :meth:`~django.db.models.query.QuerySet.prefetch_related` or
           :func:`~django.db.models.prefetch_related_objects`.

           Consider this case:

           .. testcode:: update_translations_0

              from sample.models import Continent

              # un-prefetched queryset
              europe = Continent.objects.get(code='EU')

              # first query
              europe.countries.all()[0].name = 'Germany (changed)'

              # does a second query
              new_name = europe.countries.all()[0].name

              print('Country: {}'.format(new_name))

           .. testoutput:: update_translations_0

              Country: Germany

           As we can see the new query did not fetch the changes we made
           before. To fix it:

           .. testcode:: update_translations_0

              from sample.models import Continent

              # prefetched queryset
              europe = Continent.objects.prefetch_related(
                  'countries',
              ).get(code='EU')

              # first query
              europe.countries.all()[0].name = 'Germany (changed)'

              # uses the first query
              new_name = europe.countries.all()[0].name

              print('Country: {}'.format(new_name))

           .. testoutput:: update_translations_0

              Country: Germany (changed)

        To update the translations of an instance and the relations of it:

        .. testcode:: update_translations_1

           from sample.models import Continent

           relations = ('countries', 'countries__cities',)

           europe = Continent.objects.prefetch_related(
               *relations,
           ).get(code='EU')

           print('OLD TRANSLATIONS:')
           print('-----------------')

           europe.apply_translations(
               *relations,
               lang='de',
           )

           print('Continent: {}'.format(europe))
           for country in europe.countries.all():
               print('Country: {}'.format(country))
               for city in country.cities.all():
                   print('City: {}'.format(city))

           print('\\nCHANGING...\\n')

           europe.name = 'Europa (changed)'
           europe.countries.all()[0].name = 'Deutschland (changed)'

           europe.update_translations(
               *relations,
               lang='de',
           )

           print('NEW TRANSLATIONS:')
           print('-----------------')

           europe.apply_translations(
               *relations,
               lang='de',
           )

           print('Continent: {}'.format(europe))
           for country in europe.countries.all():
               print('Country: {}'.format(country))
               for city in country.cities.all():
                   print('City: {}'.format(city))

        .. testoutput:: update_translations_1

           OLD TRANSLATIONS:
           -----------------
           Continent: Europa
           Country: Deutschland
           City: Köln
           City: München

           CHANGING...

           NEW TRANSLATIONS:
           -----------------
           Continent: Europa (changed)
           Country: Deutschland (changed)
           City: Köln
           City: München
        """
        update_translations(self, *relations, lang=lang)

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
