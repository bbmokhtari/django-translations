*********
Utilities
*********

.. module:: translations.utils

This module contains the utilities for the Translations app.

.. function:: _get_standard_language(lang)

   Return the standard language code of a custom language code.

   Searches the :data:`~django.conf.settings.LANGUAGES` in the settings for
   the custom language code, if the exact custom language code is found, it
   returns it, otherwise searches for the unaccented form of the custom
   language code, if the unaccented form of the custom language code is
   found, it returns it, otherwise it throws an error stating there is no
   such language supported in the settings.

   :param lang: The custom language code to derive the standard language code
       out of.
   :type lang: str
   :return: The standard language code derived out of the custom language
       code.
   :rtype: str
   :raise ValueError: If the language code is not specified in
       the :data:`~django.conf.settings.LANGUAGES` setting.

   Considering this setting:

   .. code-block:: python

      LANGUAGE_CODE = 'en-us'
      LANGUAGES = (
          ('en', 'English'),
          ('en-gb', 'English (Great Britain)'),
          ('de', 'German'),
          ('tr', 'Turkish'),
      )

   To get the standard language code of an unaccented language code:

   .. testcode:: _get_standard_language

      from translations.utils import _get_standard_language

      # get the standard custom language code
      custom = _get_standard_language('en')

      print(custom)

   .. testoutput:: _get_standard_language

      en

   To get the standard language code of an existing accented language code:

   .. testcode:: _get_standard_language

      from translations.utils import _get_standard_language

      # get the standard custom language code
      custom = _get_standard_language('en-gb')

      print(custom)

   .. testoutput:: _get_standard_language

      en-gb

   To get the standard language code of a non-existing accented language code:

   .. testcode:: _get_standard_language

      from translations.utils import _get_standard_language

      # get the standard custom language code
      custom = _get_standard_language('en-us')

      print(custom)

   .. testoutput:: _get_standard_language

      en

.. function:: _get_default_language()

   Return the standard language code of the default language code.

   :return: The standard language code of the default language code.
   :rtype: str
   :raise ValueError: If the default language code is not specified in
       the :data:`~django.conf.settings.LANGUAGES` setting.

   Considering this setting:

   .. code-block:: python

      LANGUAGE_CODE = 'en-us'
      LANGUAGES = (
          ('en', 'English'),
          ('en-gb', 'English (Great Britain)'),
          ('de', 'German'),
          ('tr', 'Turkish'),
      )

   To get the standard language code of the default language code:

   .. testcode:: _get_default_language

      from translations.utils import _get_default_language

      # get the standard default language code
      default = _get_default_language()

      print(default)

   .. testoutput:: _get_default_language

      en

.. function:: _get_active_language()

   Return the standard language code of the active language code.

   :return: The standard language code of the active language code.
   :rtype: str
   :raise ValueError: If the active language code is not specified in
       the :data:`~django.conf.settings.LANGUAGES` setting.

   Considering this setting:

   .. code-block:: python

      LANGUAGE_CODE = 'en-us'
      LANGUAGES = (
          ('en', 'English'),
          ('en-gb', 'English (Great Britain)'),
          ('de', 'German'),
          ('tr', 'Turkish'),
      )

   To get the standard language code of the active language code:

   .. testcode:: _get_active_language

      from translations.utils import _get_active_language

      # get the standard active language code
      active = _get_active_language()

      print(active)

   .. testoutput:: _get_active_language

      en

.. function:: _get_preferred_language(lang=None)

   Return the standard language code of a preferred language code.

   If the preferred language code is passed in, it returns the standard language
   code of it, otherwise it returns the standard language code of the active
   language code.

   :param lang: The preferred language code to derive the standard language code
       out of.
       ``None`` means use the :term:`active language` code.
   :type lang: str or None
   :return: The standard language code of the preferred language code.
   :rtype: str
   :raise ValueError: If the preferred language code is not specified in
       the :data:`~django.conf.settings.LANGUAGES` setting.

   Considering this setting:

   .. code-block:: python

      LANGUAGE_CODE = 'en-us'
      LANGUAGES = (
          ('en', 'English'),
          ('en-gb', 'English (Great Britain)'),
          ('de', 'German'),
          ('tr', 'Turkish'),
      )

   To get the standard language code of the preferred language code:

   .. testcode:: _get_preferred_language

      from translations.utils import _get_preferred_language

      # get the standard preferred language code
      preferred = _get_preferred_language()

      print(preferred)

   .. testoutput:: _get_preferred_language

      en

.. function:: _get_all_languages()

   Return all the language codes.

   Returns the list of language codes from the settings.

   :return: The language codes.
   :rtype: list(str)

   Considering this setting:

   .. code-block:: python

      LANGUAGES = (
          ('en', 'English'),
          ('en-gb', 'English (Great Britain)'),
          ('de', 'German'),
          ('tr', 'Turkish'),
      )

   To get all the language codes:

   .. testcode:: _get_all_languages

      from translations.utils import _get_all_languages

      # usage
      languages = _get_all_languages()

      # output
      print(languages)

   .. testoutput:: _get_all_languages

      [
          'en',
          'en-gb',
          'de',
          'tr',
      ]

.. function:: _get_translation_language_choices()

   Return the translation language choices.

   Returns the list of languages from the settings removing the
   default language code and adding an empty one.

   :return: The translation language choices.
   :rtype: list(tuple(str, str))
   :raise ValueError: If the default language code is not specified in
       the :data:`~django.conf.settings.LANGUAGES` setting.

   Considering this setting:

   .. code-block:: python

      LANGUAGE_CODE = 'en-us'
      LANGUAGES = (
          ('en', 'English'),
          ('en-gb', 'English (Great Britain)'),
          ('de', 'German'),
          ('tr', 'Turkish'),
      )

   To get the translation language choices:

   .. testcode:: _get_translation_language_choices

      from translations.utils import _get_translation_language_choices

      # usage
      languages = _get_translation_language_choices()

      # output
      print(languages)

   .. testoutput:: _get_translation_language_choices

      [
          (None, '---------'),
          ('en-gb', 'English (Great Britain)'),
          ('de', 'German'),
          ('tr', 'Turkish'),
      ]

.. function:: _get_reverse_relation(model, relation)

   Return the reverse of a model's relation.

   Processes the model's relation which points from the model to the target
   model and returns the reverse relation which points from the target model
   back to the model.

   :param model: The model which contains the relation and the reverse
       relation points to.
   :type model: type(~django.db.models.Model)
   :param relation: The relation of the model to get the reverse of.
       It may be composed of many ``related_query_name``\ s separated by
       :data:`~django.db.models.constants.LOOKUP_SEP` (usually ``__``) to
       represent a deeply nested relation.
   :type relation: str
   :return: The reverse of the model's relation.
   :rtype: str
   :raise ~django.core.exceptions.FieldDoesNotExist: If the relation is
       pointing to the fields that don't exist.

   To get the reverse of a model's relation:

   .. testcode:: _get_reverse_relation

      from sample.models import Continent
      from translations.utils import _get_reverse_relation

      # usage
      reverse_relation = _get_reverse_relation(Continent,
                                               'countries__cities')

      # output
      print('City can be queried with `{}`'.format(reverse_relation))

   .. testoutput:: _get_reverse_relation

      City can be queried with `country__continent`

.. function:: _get_dissected_lookup(model, lookup)

   Return the dissected info of a lookup.

   Dissects the lookup and returns comprehensive information about it,
   like what relations does it follow, what field name and field lookup does
   it contain and whether the field is translatable or not.

   :param model: The model which the lookup acts on.
   :type model: type(~django.db.models.Model)
   :param lookup: The lookup of the model to get the dissected info of.
       It may be composed of many ``related_query_name``\ s separated by
       :data:`~django.db.models.constants.LOOKUP_SEP` (usually ``__``) to
       represent a deeply nested relation.
   :type lookup: str
   :return: The dissected info of the lookup.
   :rtype: dict
   :raise ~django.core.exceptions.FieldDoesNotExist: If the relation is
       pointing to the fields that don't exist.
   :raise ~django.core.exceptions.FieldError: If the lookup is not
       supported.

   To get the dissected info of a lookup:

   .. testcode:: _get_dissected_lookup

      from sample.models import Continent
      from translations.utils import _get_dissected_lookup

      # usage
      info = _get_dissected_lookup(Continent,
                                   'countries__name__icontains')

      # output
      print(info)

   .. testoutput:: _get_dissected_lookup

      {
          'field': 'name',
          'relation': [
              'countries',
          ],
          'supplement': 'icontains',
          'translatable': True,
      }

.. function:: _get_relations_hierarchy(*relations)

   Return the :term:`relations hierarchy` of some relations.

   Creates the :term:`relations hierarchy`, splits each relation into
   different parts based on the relation depth and fills the
   :term:`relations hierarchy` with them. When all the relations are
   processed returns the :term:`relations hierarchy`.

   :param relations: The relations to derive the :term:`relations hierarchy`
       out of.
       Each relation may be composed of many ``related_query_name``\ s
       separated by :data:`~django.db.models.constants.LOOKUP_SEP`
       (usually ``__``) to represent a deeply nested relation.
   :type relations: list(str)
   :return: The :term:`relations hierarchy` derived out of the relations.
   :rtype: dict(str, dict)

   To get the :term:`relations hierarchy` of a first-level relation:

   .. testcode:: _get_relations_hierarchy

      from translations.utils import _get_relations_hierarchy

      # usage
      hierarchy = _get_relations_hierarchy('countries')

      # output
      print(hierarchy)

   .. testoutput:: _get_relations_hierarchy

      {
          'countries': {
              'included': True,
              'relations': {},
          },
      }

   To get the :term:`relations hierarchy` of a second-level relation,
   not including the first-level relation:

   .. testcode:: _get_relations_hierarchy

      from translations.utils import _get_relations_hierarchy

      # usage
      hierarchy = _get_relations_hierarchy('countries__cities')

      # output
      print(hierarchy)

   .. testoutput:: _get_relations_hierarchy

      {
          'countries': {
              'included': False,
              'relations': {
                  'cities': {
                      'included': True,
                      'relations': {},
                  },
              },
          },
      }

   To get the :term:`relations hierarchy` of a second-level relation,
   including the first-level relation:

   .. testcode:: _get_relations_hierarchy

      from translations.utils import _get_relations_hierarchy

      # usage
      hierarchy = _get_relations_hierarchy('countries',
                                           'countries__cities')

      # output
      print(hierarchy)

   .. testoutput:: _get_relations_hierarchy

      {
          'countries': {
              'included': True,
              'relations': {
                  'cities': {
                      'included': True,
                      'relations': {},
                  },
              },
          },
      }

   To get the :term:`relations hierarchy` of no relations:

   .. testcode:: _get_relations_hierarchy

      from translations.utils import _get_relations_hierarchy

      # usage
      hierarchy = _get_relations_hierarchy()

      # output
      print(hierarchy)

   .. testoutput:: _get_relations_hierarchy

      {}

.. function:: _get_entity_details(entity)

   Return the iteration and type details of an entity.

   If the entity is an iterable it returns the entity as iterable and the
   type of the first object in the iteration (since it assumes all the
   objects in the iteration are of the same type), otherwise it returns the
   entity as not iterable and the type of the entity.

   :param entity: The entity to get the details of.
   :type entity: ~django.db.models.Model or
       ~collections.Iterable(~django.db.models.Model)
   :return: The details of the entity as (iterable, model).
   :rtype: tuple(bool, type(~django.db.models.Model))
   :raise TypeError: If the entity is neither a model instance nor
       an iterable of model instances.

   .. note::

      If the entity is an empty iterable it returns the model as ``None``,
      even if the iterable is an empty queryset (which the model of can be
      retrieved). It's because the other parts of the code first check to see
      if the model in the details is ``None``, in that case they skip the
      translation process all together (because there's nothing to
      translate).

   .. testsetup:: _get_entity_details

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

   To get the details of a list of instances:

   .. testcode:: _get_entity_details

      from sample.models import Continent
      from translations.utils import _get_entity_details

      # input
      continents = list(Continent.objects.all())

      # usage
      details = _get_entity_details(continents)

      # output
      print('Iterable: {}'.format(details[0]))
      print('Model: {}'.format(details[1]))

   .. testoutput:: _get_entity_details

      Iterable: True
      Model: <class 'sample.models.Continent'>

   To get the details of a queryset:

   .. testcode:: _get_entity_details

      from sample.models import Continent
      from translations.utils import _get_entity_details

      # intput
      continents = Continent.objects.all()

      # usage
      details = _get_entity_details(continents)

      # output
      print('Iterable: {}'.format(details[0]))
      print('Model: {}'.format(details[1]))

   .. testoutput:: _get_entity_details

      Iterable: True
      Model: <class 'sample.models.Continent'>

   To get the details of an instance:

   .. testcode:: _get_entity_details

      from sample.models import Continent
      from translations.utils import _get_entity_details

      # input
      europe = Continent.objects.get(code='EU')

      # usage
      details = _get_entity_details(europe)

      # output
      print('Iterable: {}'.format(details[0]))
      print('Model: {}'.format(details[1]))

   .. testoutput:: _get_entity_details

      Iterable: False
      Model: <class 'sample.models.Continent'>

   To get the details of an empty list:

   .. testcode:: _get_entity_details

      from sample.models import Continent
      from translations.utils import _get_entity_details

      # input
      empty = []

      # usage
      details = _get_entity_details(empty)

      # output
      print('Iterable: {}'.format(details[0]))
      print('Model: {}'.format(details[1]))

   .. testoutput:: _get_entity_details

      Iterable: True
      Model: None

.. function:: _get_purview(entity, hierarchy)

   Return the :term:`purview` of an entity and
   a :term:`relations hierarchy` of it.

   Returns the mapping of the instances specified by the entity and its
   relations, and the query to fetch their translations.

   :param entity: the entity to derive the :term:`purview` out of.
   :type entity: ~django.db.models.Model or
       ~collections.Iterable(~django.db.models.Model)
   :param hierarchy: The :term:`relations hierarchy` of the entity to derive
       the :term:`purview` out of.
   :type hierarchy: dict(str, dict)
   :return: The :term:`purview` derived out of the entity and
       the :term:`relations hierarchy` of it.
   :rtype: tuple(dict(int, dict(str, ~django.db.models.Model)), \
       list(~django.db.models.Q))
   :raise TypeError:

       - If the entity is neither a model instance nor
         an iterable of model instances.

       - If the model of the entity is
         not :class:`~translations.models.Translatable`.

       - If the models of the included relations are
         not :class:`~translations.models.Translatable`.

   :raise ~django.core.exceptions.FieldDoesNotExist: If a relation is
       pointing to the fields that don't exist.

   .. testsetup:: _get_purview

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

   To get the :term:`purview` of an entity and
   the :term:`relations hierarchy` of it:

   .. testcode:: _get_purview

      from django.contrib.contenttypes.models import ContentType
      from sample.models import Continent, Country, City
      from translations.utils import _get_relations_hierarchy
      from translations.utils import _get_purview

      # input
      continents = Continent.objects.all()
      hierarchy = _get_relations_hierarchy('countries',
                                           'countries__cities')

      # usage
      mapping, query = _get_purview(continents, hierarchy)

      # output
      europe = continents[0]
      germany = europe.countries.all()[0]
      cologne = germany.cities.all()[0]

      continent = ContentType.objects.get_for_model(Continent)
      country = ContentType.objects.get_for_model(Country)
      city = ContentType.objects.get_for_model(City)

      print('Continent: `{}`'.format(
                mapping[continent.id][str(europe.id)]))
      print('Country: `{}`'.format(
                mapping[country.id][str(germany.id)]))
      print('City: `{}`'.format(
                mapping[city.id][str(cologne.id)]))

   .. testoutput:: _get_purview

      Continent: `Europe`
      Country: `Germany`
      City: `Cologne`

.. function:: _get_translations(query, lang)

   Return the translations in a language using a query.

   Queries the :class:`~translations.models.Translation` model in a language
   using the provided query and returns the queryset.

   :param query: The query to use to fetch the translations.
   :type query: list(~django.db.models.Q)
   :param lang: The language to fetch the translations in.
   :type lang: str or None
   :return: The translations in the language using the query.
   :rtype: ~django.db.models.query.QuerySet(~translations.models.Translation)

   .. testsetup:: _get_translations

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

   To get the translations of some :term:`purview`:

   .. testcode:: _get_translations

      from sample.models import Continent
      from translations.utils import _get_relations_hierarchy
      from translations.utils import _get_purview
      from translations.utils import _get_translations

      # input
      continents = list(Continent.objects.all())
      hierarchy = _get_relations_hierarchy('countries',
                                           'countries__cities',)
      mapping, query = _get_purview(continents, hierarchy)

      # usage
      translations = _get_translations(query, lang='de')

      # output
      print(translations)

   .. testoutput:: _get_translations

      <QuerySet [
          <Translation: Europe: Europa>,
          <Translation: European: Europäisch>,
          <Translation: Germany: Deutschland>,
          <Translation: German: Deutsche>,
          <Translation: Cologne: Köln>,
          <Translation: Cologner: Kölner>,
          <Translation: Asia: Asien>,
          <Translation: Asian: Asiatisch>,
          <Translation: South Korea: Südkorea>,
          <Translation: South Korean: Südkoreanisch>,
          <Translation: Seoul: Seül>,
          <Translation: Seouler: Seüler>,
      ]>
