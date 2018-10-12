*********
Utilities
*********

.. module:: translations.utils

This module contains the utilities for the Translations app.

.. function:: _get_standard_language(lang=None)

   Return the standard language code of a custom language code.

   Searches the :data:`~django.conf.settings.LANGUAGES` in the settings for
   the custom language code, if the exact custom language code is found, it
   returns it, otherwise searches for the unaccented form of the custom
   language code, if the unaccented form of the custom language code is
   found, it returns it, otherwise it throws an error stating there is no
   such language supported in the settings.

   :param lang: The custom language code to derive the standard language code
       out of.
       ``None`` means use the :term:`active language` code.
   :type lang: str or None
   :return: The standard language code derived out of the custom language
       code.
   :rtype: str
   :raise ValueError: If the language code is not specified in
       the :data:`~django.conf.settings.LANGUAGES` setting.

   .. testsetup:: _get_standard_language

      from django.utils.translation import activate

      activate('en')

   Considering this setting:

   .. code-block:: python

      LANGUAGES = (
          ('en', 'English'),
          ('en-gb', 'English (Great Britain)'),
          ('de', 'German'),
          ('tr', 'Turkish'),
      )

   To get the standard language code of the :term:`active language` code:

   .. testcode:: _get_standard_language

      from translations.utils import _get_standard_language

      # usage
      active = _get_standard_language()

      # output
      print('Language code: {}'.format(active))

   .. testoutput:: _get_standard_language

      Language code: en

   To get the standard language code of an unaccented custom language code:

   .. testcode:: _get_standard_language

      from translations.utils import _get_standard_language

      # usage
      custom = _get_standard_language('de')

      # output
      print('Language code: {}'.format(custom))

   .. testoutput:: _get_standard_language

      Language code: de

   To get the standard language code of an existing accented custom
   language code:

   .. testcode:: _get_standard_language

      from translations.utils import _get_standard_language

      # usage
      custom = _get_standard_language('en-gb')

      # output
      print('Language code: {}'.format(custom))

   .. testoutput:: _get_standard_language

      Language code: en-gb

   To get the standard language code of a non-existing accented custom
   language code:

   .. testcode:: _get_standard_language

      from translations.utils import _get_standard_language

      # usage
      custom = _get_standard_language('de-at')

      # output
      print('Language code: {}'.format(custom))

   .. testoutput:: _get_standard_language

      Language code: de

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

      [(None, '---------'), ('en-gb', 'English (Great Britain)'), ('de', 'German'), ('tr', 'Turkish')]

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
      reverse_relation = _get_reverse_relation(Continent, 'countries__cities')

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
      info = _get_dissected_lookup(Continent, 'countries__name__icontains')

      # output
      print(info)

   .. testoutput:: _get_dissected_lookup

      {'field': 'name',
       'lookup': 'icontains',
       'relation': ['countries'],
       'translatable': True}

.. function:: _get_translations_lookup_query(model, lookup, value, lang)

   Return the translations query of a lookup.

   :param model: The model which the lookup acts on.
   :type model: type(~django.db.models.Model)
   :param lookup: The lookup of the model to get the translations query
       of.
       It may be composed of many ``related_query_name``\ s separated by
       :data:`~django.db.models.constants.LOOKUP_SEP` (usually ``__``) to
       represent a deeply nested relation.
   :type lookup: str
   :param value: The value of the lookup.
   :type value: object
   :param lang: The language code of the lookup.
   :type lang: str
   :return: The translations query of the lookup.
   :rtype: ~django.db.models.Q
   :raise ~django.core.exceptions.FieldDoesNotExist: If the relation is
       pointing to the fields that don't exist.
   :raise ~django.core.exceptions.FieldError: If the lookup is not
       supported.

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

      {'countries': {'included': True, 'relations': {}}}

   To get the :term:`relations hierarchy` of a second-level relation,
   not including the first-level relation:

   .. testcode:: _get_relations_hierarchy

      from translations.utils import _get_relations_hierarchy

      # usage
      hierarchy = _get_relations_hierarchy('countries__cities')

      # output
      print(hierarchy)

   .. testoutput:: _get_relations_hierarchy

      {'countries': {'included': False,
                     'relations': {'cities': {'included': True,
                                              'relations': {}}}}}

   To get the :term:`relations hierarchy` of a second-level relation,
   including the first-level relation:

   .. testcode:: _get_relations_hierarchy

      from translations.utils import _get_relations_hierarchy

      # usage
      hierarchy = _get_relations_hierarchy('countries', 'countries__cities')

      # output
      print(hierarchy)

   .. testoutput:: _get_relations_hierarchy

      {'countries': {'included': True,
                     'relations': {'cities': {'included': True,
                                              'relations': {}}}}}

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

.. function:: _get_instance_groups(entity, hierarchy)

   Return the :term:`instance groups` of an entity and
   a :term:`relations hierarchy` of it.

   Creates the :term:`instance groups`, loops through the entity and the
   :term:`relations hierarchy` of it and fills the :term:`instance groups`
   with each instance under a certain content type. When all the instances
   are processes returns the :term:`instance groups`.

   :param entity: the entity to derive the :term:`instance groups` out of.
   :type entity: ~django.db.models.Model or
       ~collections.Iterable(~django.db.models.Model)
   :param hierarchy: The :term:`relations hierarchy` of the entity to derive
       the :term:`instance groups` out of.
   :type hierarchy: dict(str, dict)
   :return: The :term:`instance groups` derived out of the entity and
       the :term:`relations hierarchy` of it.
   :rtype: dict(int, dict(str, ~django.db.models.Model))
   :raise TypeError:

       - If the entity is neither a model instance nor
         an iterable of model instances.

       - If the model of the entity is
         not :class:`~translations.models.Translatable`.

       - If the models of the included relations are
         not :class:`~translations.models.Translatable`.

   :raise ~django.core.exceptions.FieldDoesNotExist: If a relation is
       pointing to the fields that don't exist.

   .. testsetup:: _get_instance_groups

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

   To get the :term:`instance groups` of an entity and
   the :term:`relations hierarchy` of it:

   .. testcode:: _get_instance_groups

      from django.contrib.contenttypes.models import ContentType
      from sample.models import Continent, Country, City
      from translations.utils import _get_relations_hierarchy
      from translations.utils import _get_instance_groups

      # input
      continents = Continent.objects.all()
      hierarchy = _get_relations_hierarchy('countries', 'countries__cities')

      # usage
      groups = _get_instance_groups(continents, hierarchy)

      # output
      europe = continents[0]
      germany = europe.countries.all()[0]
      cologne = germany.cities.all()[0]

      continent = ContentType.objects.get_for_model(Continent)
      country = ContentType.objects.get_for_model(Country)
      city = ContentType.objects.get_for_model(City)

      print('Continent: `{}`'.format(groups[continent.id][str(europe.id)]))
      print('Country: `{}`'.format(groups[country.id][str(germany.id)]))
      print('City: `{}`'.format(groups[city.id][str(cologne.id)]))

   .. testoutput:: _get_instance_groups

      Continent: `Europe`
      Country: `Germany`
      City: `Cologne`

.. function:: _get_translations(groups, lang)

   Return the translations of some :term:`instance groups` in a language.

   Loops through the :term:`instance groups` and collects the parameters
   that can be used to query the translations of each instance. When all
   the instances are processed it queries the
   :class:`~translations.models.Translation` model using the gathered
   parameters and returns the queryset.

   :param groups: The :term:`instance groups` to fetch the translations of.
   :type groups: dict(int, dict(str, ~django.db.models.Model))
   :param lang: The language to fetch the translations in.
       ``None`` means use the :term:`active language` code.
   :type lang: str or None
   :return: The translations of the :term:`instance groups`.
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

   To get the translations of some :term:`instance groups`:

   .. testcode:: _get_translations

      from sample.models import Continent
      from translations.utils import _get_relations_hierarchy
      from translations.utils import _get_instance_groups
      from translations.utils import _get_translations

      # input
      continents = list(Continent.objects.all())
      hierarchy = _get_relations_hierarchy('countries','countries__cities',)
      groups = _get_instance_groups(continents, hierarchy)

      # usage
      translations = _get_translations(groups, lang='de')

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
          <Translation: Seouler: Seüler>
      ]>
