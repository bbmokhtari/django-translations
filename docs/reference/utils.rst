**************
Ref: Utilities
**************

.. module:: translations.utils

This module contains the utilities for the Translations app.

.. important::

   The examples are assumed to CRUD this dataset.

   +---------------+-------------+-------------+
   | Type\\Lang    | English     | German      |
   +===============+=============+=============+
   | Continent     | Europe      | Europa      |
   |               +-------------+-------------+
   |               | Asia        | Asien       |
   +---------------+-------------+-------------+
   | Country       | Germany     | Deutschland |
   |               +-------------+-------------+
   |               | South Korea | Südkorea    |
   +---------------+-------------+-------------+
   | City          | Cologne     | Köln        |
   |               +-------------+-------------+
   |               | Seoul       | Seul        |
   +---------------+-------------+-------------+

   Please memorize this dataset in order to understand the examples better.

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

   .. testcode:: _get_reverse_relation.1

      from translations.utils import _get_reverse_relation
      from sample.models import Continent

      # get the reverse relation
      reverse_relation = _get_reverse_relation(Continent,
                                               'countries__cities')

      print('City can be queried with `{}`'.format(reverse_relation))

   .. testoutput:: _get_reverse_relation.1

      City can be queried with `country__continent`

.. function:: _get_dissected_lookup(model, lookup)

   Return the dissected info of a lookup.

   Dissects the lookup and returns comprehensive information about it,
   like what relations does it follow, what field name and
   supplementary lookup does it contain and whether the field is translatable
   or not.

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

   .. testcode:: _get_dissected_lookup.1

      from translations.utils import _get_dissected_lookup
      from sample.models import Continent

      # get the dissected lookup
      info = _get_dissected_lookup(Continent,
                                   'countries__name__icontains')

      print(info)

   .. testoutput:: _get_dissected_lookup.1

      {
          'field': 'name',
          'relation': [
              'countries',
          ],
          'supplement': 'icontains',
          'translatable': True,
      }

.. function:: _get_relations_hierarchy(*relations)

   Return the relations hierarchy of some relations.

   Transforms the relations into a relations hierarchy. Each level of
   relations hierarchy contains the relations in that level and each
   relation contains certain information, things like whether the relation is
   included or not and what are its nested relations, forming the next level
   of relations hierarchy.

   :param relations: The relations to get the relations hierarchy
       of.
       Each relation may be composed of many ``related_query_name``\ s
       separated by :data:`~django.db.models.constants.LOOKUP_SEP`
       (usually ``__``) to represent a deeply nested relation.
   :type relations: list(str)
   :return: The relations hierarchy of the relations.
   :rtype: dict(str, dict)

   To get the relations hierarchy of some relations
   (a first-level relation):

   .. testcode:: _get_relations_hierarchy.1

      from translations.utils import _get_relations_hierarchy

      # get the relations hierarchy
      hierarchy = _get_relations_hierarchy('countries')

      print(hierarchy)

   .. testoutput:: _get_relations_hierarchy.1

      {
          'countries': {
              'included': True,
              'relations': {},
          },
      }

   To get the relations hierarchy of some relations
   (a second-level relation not including the first-level relation):

   .. testcode:: _get_relations_hierarchy.2

      from translations.utils import _get_relations_hierarchy

      # get the relations hierarchy
      hierarchy = _get_relations_hierarchy('countries__cities')

      print(hierarchy)

   .. testoutput:: _get_relations_hierarchy.2

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

   To get the relations hierarchy of some relations
   (a second-level relation including the first-level relation):

   .. testcode:: _get_relations_hierarchy.3

      from translations.utils import _get_relations_hierarchy

      # get the relations hierarchy
      hierarchy = _get_relations_hierarchy('countries',
                                           'countries__cities')

      print(hierarchy)

   .. testoutput:: _get_relations_hierarchy.3

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

   To get the relations hierarchy of some relations
   (no relations):

   .. testcode:: _get_relations_hierarchy.4

      from translations.utils import _get_relations_hierarchy

      # get the relations hierarchy
      hierarchy = _get_relations_hierarchy()

      print(hierarchy)

   .. testoutput:: _get_relations_hierarchy.4

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
      retrieved).

   .. testsetup:: _get_entity_details.1

      create_doc_samples(translations=True)

   .. testsetup:: _get_entity_details.2

      create_doc_samples(translations=True)

   .. testsetup:: _get_entity_details.3

      create_doc_samples(translations=True)

   .. testsetup:: _get_entity_details.4

      create_doc_samples(translations=True)

   To get the iteration and type details of an entity
   (a list of instances):

   .. testcode:: _get_entity_details.1

      from translations.utils import _get_entity_details
      from sample.models import Continent

      continents = list(Continent.objects.all())

      # get the entity details
      details = _get_entity_details(continents)

      print('Iterable: {}'.format(details[0]))
      print('Model: {}'.format(details[1]))

   .. testoutput:: _get_entity_details.1

      Iterable: True
      Model: <class 'sample.models.Continent'>

   To get the iteration and type details of an entity
   (a queryset):

   .. testcode:: _get_entity_details.2

      from translations.utils import _get_entity_details
      from sample.models import Continent

      continents = Continent.objects.all()

      # get the entity details
      details = _get_entity_details(continents)

      print('Iterable: {}'.format(details[0]))
      print('Model: {}'.format(details[1]))

   .. testoutput:: _get_entity_details.2

      Iterable: True
      Model: <class 'sample.models.Continent'>

   To get the iteration and type details of an entity
   (an instance):

   .. testcode:: _get_entity_details.3

      from translations.utils import _get_entity_details
      from sample.models import Continent

      europe = Continent.objects.get(code='EU')

      # get the entity details
      details = _get_entity_details(europe)

      print('Iterable: {}'.format(details[0]))
      print('Model: {}'.format(details[1]))

   .. testoutput:: _get_entity_details.3

      Iterable: False
      Model: <class 'sample.models.Continent'>

   To get the iteration and type details of an entity
   (an empty list):

   .. testcode:: _get_entity_details.4

      from translations.utils import _get_entity_details
      from sample.models import Continent

      empty = []

      # get the entity details
      details = _get_entity_details(empty)

      print('Iterable: {}'.format(details[0]))
      print('Model: {}'.format(details[1]))

   .. testoutput:: _get_entity_details.4

      Iterable: True
      Model: None

.. function:: _get_purview(entity, hierarchy)

   Return the purview of an entity and
   a relations hierarchy of it.

   Returns the mapping of the instances specified by the entity and its
   relations, and the query to fetch their translations.

   :param entity: the entity to get the purview of.
   :type entity: ~django.db.models.Model or
       ~collections.Iterable(~django.db.models.Model)
   :param hierarchy: The relations hierarchy of the entity to get
       the purview of.
   :type hierarchy: dict(str, dict)
   :return: The purview of the entity and
       the relations hierarchy of it.
   :rtype: tuple(dict(int, dict(str, ~django.db.models.Model)), \
       ~django.db.models.Q)
   :raise TypeError:

       - If the entity is neither a model instance nor
         an iterable of model instances.

       - If the model of the entity is
         not :class:`~translations.models.Translatable`.

       - If the models of the relations are
         not :class:`~translations.models.Translatable`.

   :raise ~django.core.exceptions.FieldDoesNotExist: If a relation is
       pointing to the fields that don't exist.

   .. testsetup:: _get_purview.1

      create_doc_samples(translations=True)

   To get the purview of an entity and
   a relations hierarchy of it:

   .. testcode:: _get_purview.1

      from django.contrib.contenttypes.models import ContentType
      from translations.utils import _get_relations_hierarchy, _get_purview
      from sample.models import Continent, Country, City

      def ct(obj):
          return ContentType.objects.get_for_model(type(obj)).id

      def oi(obj):
          return str(obj.id)

      continents = Continent.objects.all()
      hierarchy = _get_relations_hierarchy('countries',
                                           'countries__cities')

      # get the purview
      mapping, query = _get_purview(continents, hierarchy)

      europe = continents[0]
      germany = europe.countries.all()[0]
      cologne = germany.cities.all()[0]

      print(mapping[ct(europe)][oi(europe)] is europe)
      print(mapping[ct(germany)][oi(germany)] is germany)
      print(mapping[ct(cologne)][oi(cologne)] is cologne)

   .. testoutput:: _get_purview.1

      True
      True
      True

.. function:: _get_translations(query, lang)

   Return the :class:`~translations.models.Translation` queryset of a query in
   a language.

   Queries the :class:`~translations.models.Translation` model using
   the provided query in the specified language and returns the queryset.

   :param query: The query to fetch
       the :class:`~translations.models.Translation` queryset of.
   :type query: ~django.db.models.Q
   :param lang: The language to fetch
       the :class:`~translations.models.Translation` queryset in.
   :type lang: str
   :return: The :class:`~translations.models.Translation` queryset of the
       query in the language.
   :rtype: ~django.db.models.query.QuerySet(~translations.models.Translation)

   .. testsetup:: _get_translations.1

      create_doc_samples(translations=True)

   To get the :class:`~translations.models.Translation` queryset of a query in
   a language:

   .. testcode:: _get_translations.1

      from translations.utils import _get_relations_hierarchy, _get_purview, _get_translations
      from sample.models import Continent

      continents = list(Continent.objects.all())
      hierarchy = _get_relations_hierarchy('countries',
                                           'countries__cities',)
      mapping, query = _get_purview(continents, hierarchy)

      # get the translations
      translations = _get_translations(query, 'de')

      print(translations)

   .. testoutput:: _get_translations.1

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
