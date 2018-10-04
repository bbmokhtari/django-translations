"""
This module contains the context managers for the Translations app. It
contains the following members:

:class:`TranslationContext`
    A context manager which provides custom translation functionalities.
"""

from translations.models import Translation
from translations.utils import _get_standard_language, \
    _get_relations_hierarchy, _get_instance_groups, _get_translations


__docformat__ = 'restructuredtext'


class TranslationContext:
    """
    A context manager which provides custom translation functionalities.

    Provides CRUD functionalities like :meth:`create`, :meth:`read`,
    :meth:`update` and :meth:`delete` to work with the translations and also
    some other functionalities to manage the context.

    .. note::

        It is **recommended** for the relations of the entity to be
        prefetched before using :class:`TranslationContext`, in order to reach
        optimal performance.

        To do this use
        :meth:`~django.db.models.query.QuerySet.select_related`,
        :meth:`~django.db.models.query.QuerySet.prefetch_related` or
        :func:`~django.db.models.prefetch_related_objects`.
    """

    def __init__(self, entity, *relations):
        """
        Initializes a :class:`~translations.utils.TranslationContext`.

        :param entity: The entity to use in the context.
        :type entity: ~django.db.models.Model or
            ~collections.Iterable(~django.db.models.Model)
        :param relations: The relations of the entity to use in the context.
        :type relations: list(str)
        :raise TypeError:

            - If the entity is neither a model instance nor
              an iterable of model instances.

            - If the model of the entity is
              not :class:`~translations.models.Translatable`.

            - If the models of the included relations are
              not :class:`~translations.models.Translatable`.

        :raise ~django.core.exceptions.FieldDoesNotExist: If a relation is
            pointing to the fields that don't exist.
        """
        hierarchy = _get_relations_hierarchy(*relations)
        self.groups = _get_instance_groups(entity, hierarchy)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def create(self, lang=None):
        """
        Create the translations from the context and write them to the
        database.

        Creates the translations of the entity and the specified relations
        of it in a language from their translatable
        :attr:`~translations.models.Translatable.TranslatableMeta.fields`
        and writes them to the database.

        :param lang: The language to create the translations in.
            ``None`` means use the :term:`active language` code.
        :type lang: str or None
        :raise ValueError: If the language code is not included in
            the :data:`~django.conf.settings.LANGUAGES` setting.
        :raise ~django.db.utils.IntegrityError: If duplicate translations
            are created for a specific field of a unique instance in a
            language.

        .. note::

           The translations get created based on the translatable
           :attr:`~translations.models.Translatable.TranslatableMeta.fields`
           even if they are not set in the context, so they better have a
           proper initial value.

        To create the translations of a list of instances and the relations of it:

        .. testsetup:: create_0

           from tests.sample import create_samples

           create_samples(
               continent_names=['europe', 'asia'],
               country_names=['germany', 'south korea'],
               city_names=['cologne', 'seoul'],
               langs=['de']
           )

        .. testcode:: create_0

           from django.db.models import prefetch_related_objects
           from sample.models import Continent
           from translations.context import TranslationContext

           relations = ('countries', 'countries__cities',)

           # input - fetch a list of instances like before
           continents = list(Continent.objects.all())
           prefetch_related_objects(continents, *relations)

           with TranslationContext(continents, *relations) as translations:
               # usage - create the translations
               continents[0].name = 'Europa (changed)'
               continents[0].countries.all()[0].name = 'Deutschland (changed)'
               continents[0].countries.all()[0].cities.all()[0].name = 'Köln (changed)'
               translations.create(lang='de')

               # output - use the list of instances like before
               translations.read(lang='de')
               print(continents[0])
               print(continents[0].countries.all()[0])
               print(continents[0].countries.all()[0].cities.all()[0])

        .. testoutput:: create_0

           Europa (changed)
           Deutschland (changed)
           Köln (changed)

        To create the translations of a queryset and the relations of it:

        .. testsetup:: create_1

           from tests.sample import create_samples

           create_samples(
               continent_names=['europe', 'asia'],
               country_names=['germany', 'south korea'],
               city_names=['cologne', 'seoul'],
               langs=['de']
           )

        .. testcode:: create_1

           from sample.models import Continent
           from translations.context import TranslationContext

           relations = ('countries', 'countries__cities',)

           # input - fetch a queryset like before
           continents = Continent.objects.prefetch_related(*relations)

           with TranslationContext(continents, *relations) as translations:
               # usage - create the translations
               continents[0].name = 'Europa (changed)'
               continents[0].countries.all()[0].name = 'Deutschland (changed)'
               continents[0].countries.all()[0].cities.all()[0].name = 'Köln (changed)'
               translations.create(lang='de')

               # output - use the queryset like before
               translations.read(lang='de')
               print(continents[0])
               print(continents[0].countries.all()[0])
               print(continents[0].countries.all()[0].cities.all()[0])

        .. testoutput:: create_1

           Europa (changed)
           Deutschland (changed)
           Köln (changed)

        To create the translations of an instance and the relations of it:

        .. testsetup:: create_2

           from tests.sample import create_samples

           create_samples(
               continent_names=['europe', 'asia'],
               country_names=['germany', 'south korea'],
               city_names=['cologne', 'seoul'],
               langs=['de']
           )

        .. testcode:: create_2

           from sample.models import Continent
           from translations.context import TranslationContext

           relations = ('countries', 'countries__cities',)

           # input - fetch an instance like before
           europe = Continent.objects.prefetch_related(*relations).get(code='EU')

           with TranslationContext(europe, *relations) as translations:
               # usage - create the translations
               europe.name = 'Europa (changed)'
               europe.countries.all()[0].name = 'Deutschland (changed)'
               europe.countries.all()[0].cities.all()[0].name = 'Köln (changed)'
               translations.create(lang='de')

               # output - use the list of instances like before
               translations.read(lang='de')
               print(europe)
               print(europe.countries.all()[0])
               print(europe.countries.all()[0].cities.all()[0])

        .. testoutput:: create_2

           Europa (changed)
           Deutschland (changed)
           Köln (changed)
        """
        lang = _get_standard_language(lang)
        translations = []
        for (ct_id, objs) in self.groups.items():
            for (obj_id, obj) in objs.items():
                for field in type(obj)._get_translatable_fields_names():
                    text = getattr(obj, field, None)
                    if text:
                        translations.append(
                            Translation(
                                content_type_id=ct_id,
                                object_id=obj_id,
                                field=field,
                                language=lang,
                                text=text,
                            )
                        )
        Translation.objects.bulk_create(translations)

    def read(self, lang=None):
        """
        Read the translations from the database and apply them on the context.

        Reads the translations of the entity and the specified relations
        of it in a language from the database and applies them on their
        translatable
        :attr:`~translations.models.Translatable.TranslatableMeta.fields`.

        :param lang: The language to fetch the translations in.
            ``None`` means use the :term:`active language` code.
        :type lang: str or None
        :raise ValueError: If the language code is not included in
            the :data:`~django.conf.settings.LANGUAGES` setting.

        .. note::

           If there is no translation for a field in translatable
           :attr:`~translations.models.Translatable.TranslatableMeta.fields`,
           the translation of the field falls back to the value of the field
           in the instance.

        .. testsetup:: read

           from tests.sample import create_samples

           create_samples(
               continent_names=['europe', 'asia'],
               country_names=['germany', 'south korea'],
               city_names=['cologne', 'seoul'],
               continent_fields=['name', 'denonym'],
               country_fields=['name', 'denonym'],
               city_fields=['name', 'denonym'],
               langs=['de']
           )

        To read the translations of a list of instances and the relations of it:

        .. testcode:: read

           from django.db.models import prefetch_related_objects
           from sample.models import Continent
           from translations.context import TranslationContext

           relations = ('countries', 'countries__cities',)

           # input - fetch a list of instances like before
           continents = list(Continent.objects.all())
           prefetch_related_objects(continents, *relations)

           with TranslationContext(continents, *relations) as translations:
               # usage - read the translations
               translations.read(lang='de')

               # output - use the list of instances like before
               print(continents[0])
               print(continents[0].countries.all()[0])
               print(continents[0].countries.all()[0].cities.all()[0])

        .. testoutput:: read

           Europa
           Deutschland
           Köln

        To read the translations of a queryset and the relations of it:

        .. testcode:: read

           from sample.models import Continent
           from translations.context import TranslationContext

           relations = ('countries', 'countries__cities',)

           # input - fetch a queryset like before
           continents = Continent.objects.prefetch_related(*relations)

           with TranslationContext(continents, *relations) as translations:
               # usage - read the translations
               translations.read(lang='de')

               # output - use the queryset like before
               print(continents[0])
               print(continents[0].countries.all()[0])
               print(continents[0].countries.all()[0].cities.all()[0])

        .. testoutput:: read

           Europa
           Deutschland
           Köln

        To read the translations of an instance and the relations of it:

        .. testcode:: read

           from sample.models import Continent
           from translations.context import TranslationContext

           relations = ('countries', 'countries__cities',)

           # input - fetch an instance like before
           europe = Continent.objects.prefetch_related(*relations).get(code='EU')

           with TranslationContext(europe, *relations) as translations:
               # usage - read the translations
               translations.read(lang='de')

               # output - use the instance like before
               print(europe)
               print(europe.countries.all()[0])
               print(europe.countries.all()[0].cities.all()[0])

        .. testoutput:: read

           Europa
           Deutschland
           Köln

        .. warning::

           Filtering any queryset after reading the translations will cause
           the translations of that queryset to be reset.

           .. testcode:: read

              from sample.models import Continent
              from translations.context import TranslationContext

              relations = ('countries', 'countries__cities',)

              europe = Continent.objects.prefetch_related(*relations).get(code='EU')

              with TranslationContext(europe, *relations) as translations:
                  translations.read(lang='de')

                  print(europe.name)
                  print(europe.countries.exclude(name='')[0].name + '  -- Wrong')
                  print(europe.countries.exclude(name='')[0].cities.all()[0].name + '  -- Wrong')

           .. testoutput:: read

              Europa
              Germany  -- Wrong
              Cologne  -- Wrong

           The solution is to do the filtering before reading the
           translations. To do this on the relations use
           :class:`~django.db.models.Prefetch`.

           .. testcode:: read

              from django.db.models import Prefetch
              from sample.models import Continent, Country
              from translations.context import TranslationContext

              relations = ('countries', 'countries__cities',)

              europe = Continent.objects.prefetch_related(
                  Prefetch(
                      'countries',
                      queryset=Country.objects.exclude(name=''),
                  ),
                  'countries__cities',
              ).get(code='EU')

              with TranslationContext(europe, *relations) as translations:
                  translations.read(lang='de')

                  print(europe.name)
                  print(europe.countries.all()[0].name + '  -- Correct')
                  print(europe.countries.all()[0].cities.all()[0].name + '  -- Correct')

           .. testoutput:: read

              Europa
              Deutschland  -- Correct
              Köln  -- Correct
        """
        lang = _get_standard_language(lang)
        translations = _get_translations(self.groups, lang)
        for translation in translations:
            ct_id = translation.content_type.id
            obj_id = translation.object_id
            field = translation.field
            text = translation.text
            obj = self.groups[ct_id][obj_id]
            if field in [x for x in type(obj)._get_translatable_fields_names()]:
                setattr(obj, field, text)

    def update(self, lang=None):
        """
        Update the translations from the context and write them to the
        database.

        Updates the translations of the entity and the specified relations
        of it in a language from their translatable
        :attr:`~translations.models.Translatable.TranslatableMeta.fields`
        and writes them to the database.

        :param lang: The language to update the translations in.
            ``None`` means use the :term:`active language` code.
        :type lang: str or None
        :raise ValueError: If the language code is not included in
            the :data:`~django.conf.settings.LANGUAGES` setting.

        .. note::

           The translations get updated based on the translatable
           :attr:`~translations.models.Translatable.TranslatableMeta.fields`
           even if they are not changed in the context, so they better have a
           proper initial value.

        .. note::

           Since :meth:`update`, first deletes the old translations and then
           creates the new translations, it may be a good idea to use
           :func:`atomic transactions <django.db.transaction.atomic>` in order
           to not lose old translations in case :meth:`update` throws an
           exception.

        .. testsetup:: update

           from tests.sample import create_samples

           create_samples(
               continent_names=['europe', 'asia'],
               country_names=['germany', 'south korea'],
               city_names=['cologne', 'seoul'],
               continent_fields=['name', 'denonym'],
               country_fields=['name', 'denonym'],
               city_fields=['name', 'denonym'],
               langs=['de']
           )

        To update the translations of a list of instances and the relations of it:

        .. testcode:: update

           from django.db.models import prefetch_related_objects
           from sample.models import Continent
           from translations.context import TranslationContext

           relations = ('countries', 'countries__cities',)

           # input - fetch a list of instances like before
           continents = list(Continent.objects.all())
           prefetch_related_objects(continents, *relations)

           with TranslationContext(continents, *relations) as translations:
               # prepare - set initial value for the context
               translations.read(lang='de')

               # usage - update the translations
               continents[0].name = 'Europa (changed)'
               continents[0].countries.all()[0].name = 'Deutschland (changed)'
               continents[0].countries.all()[0].cities.all()[0].name = 'Köln (changed)'
               translations.update(lang='de')

               # output - use the list of instances like before
               translations.read(lang='de')
               print(continents[0])
               print(continents[0].countries.all()[0])
               print(continents[0].countries.all()[0].cities.all()[0])

        .. testoutput:: update

           Europa (changed)
           Deutschland (changed)
           Köln (changed)

        To update the translations of a queryset and the relations of it:

        .. testcode:: update

           from sample.models import Continent
           from translations.context import TranslationContext

           relations = ('countries', 'countries__cities',)

           # input - fetch a queryset like before
           continents = Continent.objects.prefetch_related(*relations)

           with TranslationContext(continents, *relations) as translations:
               # prepare - set initial value for the context
               translations.read(lang='de')

               # usage - update the translations
               continents[0].name = 'Europa (changed)'
               continents[0].countries.all()[0].name = 'Deutschland (changed)'
               continents[0].countries.all()[0].cities.all()[0].name = 'Köln (changed)'
               translations.update(lang='de')

               # output - use the queryset like before
               translations.read(lang='de')
               print(continents[0])
               print(continents[0].countries.all()[0])
               print(continents[0].countries.all()[0].cities.all()[0])

        .. testoutput:: update

           Europa (changed)
           Deutschland (changed)
           Köln (changed)

        To update the translations of an instance and the relations of it:

        .. testcode:: update

           from sample.models import Continent
           from translations.context import TranslationContext

           relations = ('countries', 'countries__cities',)

           # input - fetch an instance like before
           europe = Continent.objects.prefetch_related(*relations).get(code='EU')

           with TranslationContext(europe, *relations) as translations:
               # prepare - set initial value for the context
               translations.read(lang='de')

               # usage - update the translations
               europe.name = 'Europa (changed)'
               europe.countries.all()[0].name = 'Deutschland (changed)'
               europe.countries.all()[0].cities.all()[0].name = 'Köln (changed)'
               translations.update(lang='de')

               # output - use the list of instances like before
               translations.read(lang='de')
               print(europe)
               print(europe.countries.all()[0])
               print(europe.countries.all()[0].cities.all()[0])

        .. testoutput:: update

           Europa (changed)
           Deutschland (changed)
           Köln (changed)
        """
        self.delete(lang)
        self.create(lang)

    def delete(self, lang=None):
        """
        Collect the translations from the context and delete them from the
        database.

        Collects the translations of the entity and the specified relations
        of it in a language using their translatable
        :attr:`~translations.models.Translatable.TranslatableMeta.fields`
        and deletes them from the database.

        :param lang: The language to delete the translations in.
            ``None`` means use the :term:`active language` code.
        :type lang: str or None
        :raise ValueError: If the language code is not included in
            the :data:`~django.conf.settings.LANGUAGES` setting.

        To delete the translations of a list of instances and the relations of it:

        .. testsetup:: delete_0

           from tests.sample import create_samples

           create_samples(
               continent_names=['europe', 'asia'],
               country_names=['germany', 'south korea'],
               city_names=['cologne', 'seoul'],
               continent_fields=['name', 'denonym'],
               country_fields=['name', 'denonym'],
               city_fields=['name', 'denonym'],
               langs=['de']
           )

        .. testcode:: delete_0

           from django.db.models import prefetch_related_objects
           from sample.models import Continent
           from translations.context import TranslationContext

           relations = ('countries', 'countries__cities',)

           # input - fetch a list of instances like before
           continents = list(Continent.objects.all())
           prefetch_related_objects(continents, *relations)

           with TranslationContext(continents, *relations) as translations:
               # usage - delete the translations
               translations.delete(lang='de')

               # output - use the list of instances like before
               translations.read(lang='de')
               print(continents[0])
               print(continents[0].countries.all()[0])
               print(continents[0].countries.all()[0].cities.all()[0])

        .. testoutput:: delete_0

           Europe
           Germany
           Cologne

        To delete the translations of a queryset and the relations of it:

        .. testsetup:: delete_1

           from tests.sample import create_samples

           create_samples(
               continent_names=['europe', 'asia'],
               country_names=['germany', 'south korea'],
               city_names=['cologne', 'seoul'],
               continent_fields=['name', 'denonym'],
               country_fields=['name', 'denonym'],
               city_fields=['name', 'denonym'],
               langs=['de']
           )

        .. testcode:: delete_1

           from sample.models import Continent
           from translations.context import TranslationContext

           relations = ('countries', 'countries__cities',)

           # input - fetch a queryset like before
           continents = Continent.objects.prefetch_related(*relations)

           with TranslationContext(continents, *relations) as translations:
               # usage - delete the translations
               translations.delete(lang='de')

               # output - use the queryset like before
               translations.read(lang='de')
               print(continents[0])
               print(continents[0].countries.all()[0])
               print(continents[0].countries.all()[0].cities.all()[0])

        .. testoutput:: delete_1

           Europe
           Germany
           Cologne

        To delete the translations of an instance and the relations of it:

        .. testsetup:: delete_2

           from tests.sample import create_samples

           create_samples(
               continent_names=['europe', 'asia'],
               country_names=['germany', 'south korea'],
               city_names=['cologne', 'seoul'],
               continent_fields=['name', 'denonym'],
               country_fields=['name', 'denonym'],
               city_fields=['name', 'denonym'],
               langs=['de']
           )

        .. testcode:: delete_2

           from sample.models import Continent
           from translations.context import TranslationContext

           relations = ('countries', 'countries__cities',)

           # input - fetch an instance like before
           europe = Continent.objects.prefetch_related(*relations).get(code='EU')

           with TranslationContext(europe, *relations) as translations:
               # usage - delete the translations
               translations.delete(lang='de')

               # output - use the list of instances like before
               translations.read(lang='de')
               print(europe)
               print(europe.countries.all()[0])
               print(europe.countries.all()[0].cities.all()[0])

        .. testoutput:: delete_2

           Europe
           Germany
           Cologne
        """
        lang = _get_standard_language(lang)
        translations = _get_translations(self.groups, lang)
        translations.delete()

    def reset(self):
        """
        Reset the translations of the context to the original values.

        Resets the translations of the entity and the specified relations
        of it on their translatable
        :attr:`~translations.models.Translatable.TranslatableMeta.fields`.

        .. testsetup:: reset

           from tests.sample import create_samples

           create_samples(
               continent_names=['europe', 'asia'],
               country_names=['germany', 'south korea'],
               city_names=['cologne', 'seoul'],
               continent_fields=['name', 'denonym'],
               country_fields=['name', 'denonym'],
               city_fields=['name', 'denonym'],
               langs=['de']
           )

        To reset the translations of a list of instances and the relations of it:

        .. testcode:: reset

           from django.db.models import prefetch_related_objects
           from sample.models import Continent
           from translations.context import TranslationContext

           relations = ('countries', 'countries__cities',)

           # input - fetch a list of instances like before
           continents = list(Continent.objects.all())
           prefetch_related_objects(continents, *relations)

           with TranslationContext(continents, *relations) as translations:
               translations.read(lang='de')
  
               # usage - reset the translations
               translations.reset()

               # output - use the list of instances like before
               print(continents[0])
               print(continents[0].countries.all()[0])
               print(continents[0].countries.all()[0].cities.all()[0])

        .. testoutput:: reset

           Europe
           Germany
           Cologne

        To reset the translations of a queryset and the relations of it:

        .. testcode:: reset

           from sample.models import Continent
           from translations.context import TranslationContext

           relations = ('countries', 'countries__cities',)

           # input - fetch a queryset like before
           continents = Continent.objects.prefetch_related(*relations)

           with TranslationContext(continents, *relations) as translations:
               translations.read(lang='de')

               # usage - reset the translations
               translations.reset()

               # output - use the queryset like before
               print(continents[0])
               print(continents[0].countries.all()[0])
               print(continents[0].countries.all()[0].cities.all()[0])

        .. testoutput:: reset

           Europe
           Germany
           Cologne

        To reset the translations of an instance and the relations of it:

        .. testcode:: reset

           from sample.models import Continent
           from translations.context import TranslationContext

           relations = ('countries', 'countries__cities',)

           # input - fetch an instance like before
           europe = Continent.objects.prefetch_related(*relations).get(code='EU')

           with TranslationContext(europe, *relations) as translations:
               translations.read(lang='de')

               # usage - reset the translations
               translations.reset()

               # output - use the instance like before
               print(europe)
               print(europe.countries.all()[0])
               print(europe.countries.all()[0].cities.all()[0])

        .. testoutput:: reset

           Europe
           Germany
           Cologne
        """
        for (ct_id, objs) in self.groups.items():
            for (obj_id, obj) in objs.items():
                for (field, value) in obj._default_translatable_fields.items():
                    setattr(obj, field, value)
