"""
This module contains the utilities for the Translations app.

.. rubric:: Functions:

:func:`get_translation_language`
    Return the language code for the translation process.
:func:`get_entity_details`
    Return the details of an entity.
:func:`get_reverse_relation`
    Return the reverse of a relation for a model.
:func:`get_translations_reverse_relation`
    Return the reverse of the translations relation of a relation for a model.
:func:`get_translations`
    Return the translations of an entity and the relations of it in a language.
:func:`get_translations_dictionary`
    Return the translations dictionary out of some translations.
:func:`fill_hierarchy`
    Fills a relations hierarchy with parts of a relation.
:func:`get_relations_hierarchy`
    Return the relations hierarchy of some relations.
:func:`apply_obj_translations`
    Apply translations dictionary on an object.
:func:`apply_rel_translations`
    Apply translations dictionary on a relations hierarchy of an object.
:func:`read_translations`
    Translate an entity and the relations of it in a language.
"""

from django.db import models, transaction
from django.db.models.constants import LOOKUP_SEP
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import get_language
from django.conf import settings

import translations.models


__docformat__ = 'restructuredtext'


def get_translation_language(lang=None):
    """
    Return the language code for the translation process.

    If the ``lang`` parameter is not passed in, it returns the active language
    code [#active_language]_, otherwise it returns the custom language code
    indicated by the ``lang`` parameter.

    :param lang: A custom language code.
        ``None`` means use the active language code.
    :type lang: str or None
    :return: The language code for the translation process.
    :rtype: str
    :raise ValueError: If the language code is not specified in
        the :data:`~django.conf.settings.LANGUAGES` setting.

    .. [#active_language]
       The active language code is a language code determined automatically
       by Django. It is not a global system-wide setting, but it is rather a
       per-request setting, usually determined by the ``Accept-Language``
       header received in each HTTP request (by the browser or another
       client). You can access it using
       :func:`~django.utils.translation.get_language` in each view.

    .. testsetup:: get_translation_language

       from django.utils.translation import activate

       activate('en')

    To get the active language code requested by the client:

    .. testcode:: get_translation_language

       from translations.utils import get_translation_language

       active = get_translation_language()
       print("Language code: {}".format(active))

    .. testoutput:: get_translation_language

       Language code: en

    To get a custom language code other than what the client might have
    requested:

    .. testcode:: get_translation_language

       from translations.utils import get_translation_language

       custom = get_translation_language('de')
       print("Language code: {}".format(custom))

    .. testoutput:: get_translation_language

       Language code: de
    """
    lang = lang if lang else get_language()

    if lang not in [language[0] for language in settings.LANGUAGES]:
        raise ValueError(
            "The language code `{}` is not supported.".format(lang)
        )

    return lang


def get_entity_details(entity):
    """
    Return the details of an entity.

    Determines if an entity is iterable or not, if so it returns the type of
    the first object in the iteration (since it assumes all the objects in the
    iteration are of the same type), otherwise it returns the type of the
    entity itself.

    :param entity: The entity to get the details of.
    :type entity: ~django.db.models.Model or
        ~collections.Iterable(~django.db.models.Model)
    :return: The entity details as (model, iterable).
    :rtype: tuple(type(~django.db.models.Model), bool)
    :raise TypeError: If the entity is neither a model instance nor
        an iterable of model instances.

    .. testsetup:: get_entity_details

       from tests.sample import create_samples

       create_samples(continent_names=["europe"])

    To get the details of a list of model instances:

    .. testcode:: get_entity_details

       from sample.models import Continent
       from translations.utils import get_entity_details

       continents = list(Continent.objects.all())
       details = get_entity_details(continents)
       print("Model: {}".format(details[0]))
       print("Iterable: {}".format(details[1]))

    .. testoutput:: get_entity_details

       Model: <class 'sample.models.Continent'>
       Iterable: True

    To get the details of a queryset:

    .. testcode:: get_entity_details

       from sample.models import Continent
       from translations.utils import get_entity_details

       continents = Continent.objects.all()
       details = get_entity_details(continents)
       print("Model: {}".format(details[0]))
       print("Iterable: {}".format(details[1]))

    .. testoutput:: get_entity_details

       Model: <class 'sample.models.Continent'>
       Iterable: True

    To get the details of a model instance:

    .. testcode:: get_entity_details

       from sample.models import Continent
       from translations.utils import get_entity_details

       europe = Continent.objects.get(code="EU")
       details = get_entity_details(europe)
       print("Model: {}".format(details[0]))
       print("Iterable: {}".format(details[1]))

    .. testoutput:: get_entity_details

       Model: <class 'sample.models.Continent'>
       Iterable: False

    .. note::
       An empty iterable returns the model as ``None``, even if the iterable
       is an empty queryset, though the model for it can be retrieved. It's
       because other parts of the code first check to see if details model is
       ``None``, in that case they skip the translation process all together,
       because there's nothing to translate.

       .. testcode:: get_entity_details

           from sample.models import Continent
           from translations.utils import get_entity_details

           empty = []
           details = get_entity_details(empty)
           print("Model: {}".format(details[0]))
           print("Iterable: {}".format(details[1]))

       .. testoutput:: get_entity_details

          Model: None
          Iterable: True
    """
    error_message = '`{}` is neither {} nor {}.'.format(
        entity,
        'a model instance',
        'an iterable of model instances'
    )

    if isinstance(entity, models.Model):
        model = type(entity)
        iterable = False
    elif hasattr(entity, '__iter__'):
        if len(entity) > 0:
            if isinstance(entity[0], models.Model):
                model = type(entity[0])
            else:
                raise TypeError(error_message)
        else:
            model = None
        iterable = True
    else:
        raise TypeError(error_message)

    return model, iterable


def get_reverse_relation(model, relation):
    """
    Return the reverse of a relation for a model.

    Checks a relation of a model (which points to a target model) and returns
    a relation which the target model can use to fetch the target model
    instances using an initial model instance.

    :param model: The model which contains the relation and the reverse
        relation points to.
    :type model: type(~django.db.models.Model)
    :param relation: The relation of the model to get the reverse of.
        It may be composed of many ``related_query_name`` separated by
        :data:`~django.db.models.constants.LOOKUP_SEP` (usually ``__``) to
        represent a deeply nested relation.
    :type relation: str
    :return: The reverse of the relation.
    :rtype: str
    :raise ~django.core.exceptions.FieldDoesNotExist: If the relation is
        pointing to the fields that don't exist.

    .. testsetup:: get_reverse_relation

       from tests.sample import create_samples

       create_samples(
           continent_names=["europe"],
           country_names=["germany"],
           city_names=["cologne", "munich"]
       )

    Let's suppose in some part of a program a list of all the cities in a
    continent must be outputted.

    Instead of doing:

    .. testcode:: get_reverse_relation

       from sample.models import Continent

       europe = Continent.objects.get(code="EU")

       for country in europe.countries.all():
           print(country.cities.all())

    .. testoutput:: get_reverse_relation

       <TranslatableQuerySet [<City: Cologne>, <City: Munich>]>

    Which does a *minimum* of two queries to the database (one for the
    countries and one for the cities) even if the
    :meth:`~django.db.models.query.QuerySet.prefetch_related` is used, the
    same can be achieved with:

    .. testcode:: get_reverse_relation

       from sample.models import Continent, City
       from translations.utils import get_reverse_relation

       europe = Continent.objects.get(code="EU")

       reverse_relation = get_reverse_relation(Continent, 'countries__cities')
       print("City can be queried with '{}'".format(reverse_relation))

       cities = City.objects.filter(**{reverse_relation: europe})
       print(cities)

    .. testoutput:: get_reverse_relation

       City can be queried with 'country__continent'
       <TranslatableQuerySet [<City: Cologne>, <City: Munich>]>

    Which on the contrary does only *one* query to the database.
    """
    parts = relation.split(LOOKUP_SEP)
    root = parts[0]
    branch = parts[1:]

    field = model._meta.get_field(root)
    reverse_relation = field.remote_field.name

    if branch:
        branch_model = field.related_model
        branch_relation = LOOKUP_SEP.join(branch)
        branch_reverse_relation = get_reverse_relation(
            branch_model,
            branch_relation
        )
        return '{}__{}'.format(
            branch_reverse_relation,
            reverse_relation
        )
    else:
        return reverse_relation


def get_translations_reverse_relation(model, relation=None):
    """
    Return the reverse of the translations relation of a relation for a model.

    If the ``relation`` parameter is not passed in, it checks the
    ``translations`` relation of the model (which points to the
    :class:`~translations.models.Translation` model) and returns a relation
    which the :class:`~translations.models.Translation` model can use to fetch
    the translations for the model using a model instance, otherwise
    it checks the ``translations`` relation of the ``relation`` of the model,
    which points to the :class:`~translations.models.Translation` model and
    returns a relation which the :class:`~translations.models.Translation`
    model can use to fetch the translations for the relation of the model
    using a model instance.

    :param model: The model which contains the ``translations`` relation
        directly or indirectly (either it contains the ``translations``
        relation itself, or the specified relation contains it) and which the
        reverse relation points to.
    :type model: type(~django.db.models.Model)
    :param relation: The relation of the model which contains the
        ``translations`` relation, to get the reverse of.
        It may be composed of many ``related_query_name`` separated by
        :data:`~django.db.models.constants.LOOKUP_SEP` (usually ``__``) to
        represent a deeply nested relation.
        ``None`` means the reverse relation of the ``translations`` relation
        should be returned for the model itself.
    :type relation: str or None
    :return: The reverse of the translations relation.
    :rtype: str
    :raise ~django.core.exceptions.FieldDoesNotExist: If the relation is
        pointing to the fields that don't exist.

    .. testsetup:: get_translations_reverse_relation

       from tests.sample import create_samples

       create_samples(
           continent_names=["europe"],
           country_names=["germany"],
           city_names=["cologne", "munich"],
           continent_fields=["name", "denonym"],
           country_fields=["name", "denonym"],
           city_fields=["name", "denonym"],
           langs=["de"]
       )

    Let's suppose in some part of a program the translations of all the cities
    in a continent must be outputted.

    Instead of doing:

    .. testcode:: get_translations_reverse_relation

       from sample.models import Continent

       europe = Continent.objects.get(code="EU")

       for country in europe.countries.all():
           for city in country.cities.all():
               print(city.translations.all())

    .. testoutput:: get_translations_reverse_relation

       <QuerySet [
           <Translation: Cologner: Kölner>,
           <Translation: Cologne: Köln>
       ]>
       <QuerySet [
           <Translation: Munichian: Münchner>,
           <Translation: Munich: München>
       ]>

    Which does a *minimum* of three queries to the database (one for the
    countries, one for the cities and one for the translations) even if the
    :meth:`~django.db.models.query.QuerySet.prefetch_related` is used, the
    same can be achieved with:

    .. testcode:: get_translations_reverse_relation

       from sample.models import Continent
       from translations.models import Translation
       from translations.utils import get_translations_reverse_relation

       europe = Continent.objects.get(code="EU")

       reverse_relation = get_translations_reverse_relation(
           Continent, 'countries__cities')
       print("Translation can be queried with '{}'".format(reverse_relation))

       translations = Translation.objects.filter(**{reverse_relation: europe})
       print(translations)

    .. testoutput:: get_translations_reverse_relation

       Translation can be queried with 'sample_city__country__continent'
       <QuerySet [
           <Translation: Cologne: Köln>,
           <Translation: Cologner: Kölner>,
           <Translation: Munich: München>,
           <Translation: Munichian: Münchner>
       ]>

    Which on the contrary does only *one* query to the database.

    Also if the translations of the continent must be outputted:

    .. testcode:: get_translations_reverse_relation

       from sample.models import Continent
       from translations.models import Translation
       from translations.utils import get_translations_reverse_relation

       europe = Continent.objects.get(code="EU")

       reverse_relation = get_translations_reverse_relation(Continent)
       print("Translation can be queried with '{}'".format(reverse_relation))

       translations = Translation.objects.filter(**{reverse_relation: europe})
       print(translations)

    .. testoutput:: get_translations_reverse_relation

       Translation can be queried with 'sample_continent'
       <QuerySet [
           <Translation: Europe: Europa>,
           <Translation: European: Europäisch>
       ]>
    """
    if relation is None:
        translations_relation = 'translations'
    else:
        translations_relation = '{}__{}'.format(relation, 'translations')

    return get_reverse_relation(model, translations_relation)


def get_translations(entity, *relations, lang=None):
    """
    Return the translations of an entity and the relations of it in a language.

    Collects all the translations of the entity and the specified relations
    of it in a language and return them as a
    :class:`~translations.models.Translation` queryset.

    :param entity: The entity to fetch the translations for.
    :type entity: ~django.db.models.Model or
        ~collections.Iterable(~django.db.models.Model)
    :param relations: The relations of the entity to fetch the
        translations for.
    :type relations: list(str)
    :param lang: The language to fetch the translations in.
        ``None`` means use the active language code. [#active_language]_
    :type lang: str or None
    :return: The :class:`~translations.models.Translation` queryset.
    :rtype: ~django.db.models.query.QuerySet
    :raise ValueError: If the language code is not included in
        the :data:`~django.conf.settings.LANGUAGES` setting.
    :raise TypeError: If the entity is neither a model instance nor
        an iterable of model instances.
    :raise ~django.core.exceptions.FieldDoesNotExist: If a relation is
        pointing to the fields that don't exist.

    .. testsetup:: get_translations

       from tests.sample import create_samples

       create_samples(
           continent_names=["europe", "asia"],
           country_names=["germany", "south korea"],
           city_names=["cologne", "munich", "seoul", "ulsan"],
           continent_fields=["name", "denonym"],
           country_fields=["name", "denonym"],
           city_fields=["name", "denonym"],
           langs=["de"]
       )

    To get the translations of a list of model instances:

    .. testcode:: get_translations

       from sample.models import Continent, Country, City
       from translations.utils import get_translations

       continents = Continent.objects.prefetch_related(
           'countries', 'countries__cities'
       ).all()

       continents = list(continents)

       translations = get_translations(
           continents,
           "countries", "countries__cities",
           lang="de"
       )

       print(translations)

    .. testoutput:: get_translations

       <QuerySet [
           <Translation: Europe: Europa>,
           <Translation: European: Europäisch>,
           <Translation: Germany: Deutschland>,
           <Translation: German: Deutsche>,
           <Translation: Cologne: Köln>,
           <Translation: Cologner: Kölner>,
           <Translation: Munich: München>,
           <Translation: Munichian: Münchner>,
           <Translation: Asia: Asien>,
           <Translation: Asian: Asiatisch>,
           <Translation: South Korea: Südkorea>,
           <Translation: South Korean: Südkoreanisch>,
           <Translation: Seoul: Seül>,
           <Translation: Seouler: Seülisch>,
           <Translation: Ulsan: Ulsän>,
           <Translation: Ulsanian: Ulsänisch>
       ]>

    To get the translations of a queryset:

    .. testcode:: get_translations

       from sample.models import Continent, Country, City
       from translations.utils import get_translations

       continents = Continent.objects.prefetch_related(
           'countries', 'countries__cities'
       ).all()

       translations = get_translations(
           continents,
           "countries", "countries__cities",
           lang="de"
       )

       print(translations)

    .. testoutput:: get_translations

       <QuerySet [
           <Translation: Europe: Europa>,
           <Translation: European: Europäisch>,
           <Translation: Germany: Deutschland>,
           <Translation: German: Deutsche>,
           <Translation: Cologne: Köln>,
           <Translation: Cologner: Kölner>,
           <Translation: Munich: München>,
           <Translation: Munichian: Münchner>,
           <Translation: Asia: Asien>,
           <Translation: Asian: Asiatisch>,
           <Translation: South Korea: Südkorea>,
           <Translation: South Korean: Südkoreanisch>,
           <Translation: Seoul: Seül>,
           <Translation: Seouler: Seülisch>,
           <Translation: Ulsan: Ulsän>,
           <Translation: Ulsanian: Ulsänisch>
       ]>

    To get the translations of a model instance:

    .. testcode:: get_translations

       from sample.models import Continent, Country, City
       from translations.utils import get_translations

       europe = Continent.objects.prefetch_related(
           'countries', 'countries__cities'
       ).get(code="EU")

       translations = get_translations(
           europe,
           "countries", "countries__cities",
           lang="de"
       )

       print(translations)

    .. testoutput:: get_translations

       <QuerySet [
           <Translation: Europe: Europa>,
           <Translation: European: Europäisch>,
           <Translation: Germany: Deutschland>,
           <Translation: German: Deutsche>,
           <Translation: Cologne: Köln>,
           <Translation: Cologner: Kölner>,
           <Translation: Munich: München>,
           <Translation: Munichian: Münchner>
       ]>
    """
    lang = get_translation_language(lang)
    model, iterable = get_entity_details(entity)

    if model is None:
        return translations.models.Translation.objects.none()

    if iterable:
        condition = 'pk__in'
        value = [instance.pk for instance in entity]
    else:
        condition = 'pk'
        value = entity.pk

    queries = []

    if issubclass(model, translations.models.Translatable):
        trans = get_translations_reverse_relation(model)
        prop = '{}__{}'.format(trans, condition)
        queries.append(
            models.Q(**{prop: value})
        )

    for relation in relations:
        trans = get_translations_reverse_relation(model, relation)
        prop = '{}__{}'.format(trans, condition)
        queries.append(
            models.Q(**{prop: value})
        )

    if len(queries) == 0:
        return translations.models.Translation.objects.none()

    filters = queries.pop()
    for query in queries:
        filters |= query

    queryset = translations.models.Translation.objects.filter(
        language=lang
    ).filter(
        filters
    ).distinct().select_related('content_type')

    return queryset


def get_translations_dictionary(translations):
    """
    Return the translations dictionary out of some translations.

    Processes the translations and returns the :term:`translations dictionary`
    to use for the translation process.

    :param translations: The translations to process.
    :type translations: ~django.db.models.query.QuerySet
    :return: The translations dictionary.
    :rtype: dict(int, dict(str, dict(str, str)))

    .. warning::
       Always filter the ``translations`` in a language before passing it in,
       otherwise the other language may override some fields of the initial
       language and a translations dictionary with mixed content gets
       outputted which is not what's desired.

    .. testsetup:: get_translations_dictionary

       from tests.sample import create_samples

       create_samples(
           continent_names=["europe", "asia"],
           country_names=["germany", "south korea"],
           city_names=["cologne", "munich", "seoul", "ulsan"],
           continent_fields=["name", "denonym"],
           country_fields=["name", "denonym"],
           city_fields=["name", "denonym"],
           langs=["de"]
       )

    To get the translations dictionary of all the translations.

    .. testcode:: get_translations_dictionary

       from django.contrib.contenttypes.models import ContentType
       from sample.models import Continent, Country, City
       from translations.utils import get_translations_dictionary
       from translations.models import Translation

       translations = Translation.objects.filter(language="de")
       dictionary = get_translations_dictionary(translations)

       continent_ct = ContentType.objects.get_for_model(Continent).id
       print("Continent translations:")
       print(dictionary[continent_ct])

       country_ct = ContentType.objects.get_for_model(Country).id
       print("Country translations:")
       print(dictionary[country_ct])

       city_ct = ContentType.objects.get_for_model(City).id
       print("City translations:")
       print(dictionary[city_ct])

    .. testoutput:: get_translations_dictionary

       Continent translations:
       {'1': {'denonym': 'Europäisch', 'name': 'Europa'},
        '2': {'denonym': 'Asiatisch', 'name': 'Asien'}}
       Country translations:
       {'1': {'denonym': 'Deutsche', 'name': 'Deutschland'},
        '2': {'denonym': 'Südkoreanisch', 'name': 'Südkorea'}}
       City translations:
       {'1': {'denonym': 'Kölner', 'name': 'Köln'},
        '2': {'denonym': 'Münchner', 'name': 'München'},
        '3': {'denonym': 'Seülisch', 'name': 'Seül'},
        '4': {'denonym': 'Ulsänisch', 'name': 'Ulsän'}}
    """
    dictionary = {}

    for translation in translations:
        content_type_id = translation.content_type.id
        object_id = translation.object_id
        field = translation.field

        dictionary.setdefault(content_type_id, {})
        dictionary[content_type_id].setdefault(object_id, {})

        dictionary[content_type_id][object_id][field] = translation.text

    return dictionary


def fill_hierarchy(hierarchy, *relation_parts):
    """
    Fills a relations hierarchy with parts of a relation.

    Fills the :term:`relations hierarchy` based on the order of the parts of
    the relation. The later parts are considered as the children of the
    earlier ones. Only the parts that have filled the hierarchy as the last
    part are considered included and all the other ones are considered
    excluded.

    :param hierarchy: The relations hierarchy to fill.
    :type hierarchy: dict(str, dict)
    :param relation_parts: The relation parts sorted by the order to fill the
        relations hierarchy with.
    :type relation_parts: list(str)

    To fill the hierarchy with only one level of relation parts:

    .. testcode:: fill_hierarchy

       from translations.utils import fill_hierarchy

       hierarchy = {}

       fill_hierarchy(hierarchy, 'countries')

       print(hierarchy)

    .. testoutput:: fill_hierarchy

       {'countries': {'included': True, 'relations': {}}}

    To fill the hierarchy with two level of relation parts, not including the
    first one:

    .. testcode:: fill_hierarchy

       from translations.utils import fill_hierarchy

       hierarchy = {}

       fill_hierarchy(hierarchy, 'countries', 'cities')

       print(hierarchy)

    .. testoutput:: fill_hierarchy

       {'countries': {'included': False,
                      'relations': {'cities': {'included': True,
                                               'relations': {}}}}}

    To fill the hierarchy with two level of relation parts, including the
    first one:

    .. testcode:: fill_hierarchy

       from translations.utils import fill_hierarchy

       hierarchy = {}

       fill_hierarchy(hierarchy, 'countries')
       fill_hierarchy(hierarchy, 'countries', 'cities')

       print(hierarchy)

    .. testoutput:: fill_hierarchy

       {'countries': {'included': True,
                      'relations': {'cities': {'included': True,
                                               'relations': {}}}}}
    """
    root = relation_parts[0]
    nest = relation_parts[1:]

    hierarchy.setdefault(root, {
        "included": False,
        "relations": {}
    })

    if nest:
        fill_hierarchy(hierarchy[root]["relations"], *nest)
    else:
        hierarchy[root]["included"] = True


def get_relations_hierarchy(*relations):
    """
    Return the relations hierarchy of some relations.

    Processes the relations and returns a :term:`relations hierarchy`,
    containing each level of relation and information about whether they are
    included or not.

    :param relations: The relations to get the hierarchy of.
    :type relations: list(str)
    :return: The relations hierarchy.
    :rtype: dict(str, dict)

    To get the hierarchy of a first-level relation:

    .. testcode::

       from translations.utils import get_relations_hierarchy

       print(get_relations_hierarchy('countries'))

    .. testoutput::

       {'countries': {'included': True, 'relations': {}}}

    To get the hierarchy of a second-level relation, not including
    the first-level relation:

    .. testcode::

       from translations.utils import get_relations_hierarchy

       print(get_relations_hierarchy('countries__cities'))

    .. testoutput::

       {'countries': {'included': False,
                      'relations': {'cities': {'included': True,
                                               'relations': {}}}}}

    To get the hierarchy of a second-level relation, including the first-level
    relation:

    .. testcode::

       from translations.utils import get_relations_hierarchy

       print(get_relations_hierarchy('countries', 'countries__cities'))

    .. testoutput::

       {'countries': {'included': True,
                      'relations': {'cities': {'included': True,
                                               'relations': {}}}}}

    To get the hierarchy of no relations:

    .. testcode::

       from translations.utils import get_relations_hierarchy

       print(get_relations_hierarchy())

    .. testoutput::

       {}
    """
    hierarchy = {}
    for relation in relations:
        parts = relation.split(LOOKUP_SEP)
        fill_hierarchy(hierarchy, *parts)
    return hierarchy


def apply_obj_translations(obj, ct_dictionary, included=True):
    """
    Apply translations dictionary on an object.

    Searches the content type of the :term:`translations dictionary` for the
    translations of the object and applies them on the object, field by field
    and in place.

    :param obj: The object to apply the translations dictionary on.
    :type obj: ~django.db.models.Model
    :param ct_dictionary: The content type of translations dictionary.
    :type ct_dictionary: dict(str, dict(str, str))
    :param included: Whether to apply the translations dictionary or not.
    :type included: bool

    .. testsetup:: apply_obj_translations

       from tests.sample import create_samples

       create_samples(
           continent_names=["europe"],
           continent_fields=["name", "denonym"],
           langs=["de"]
       )

    To apply the translations dictionary on an object:

    .. testcode:: apply_obj_translations

       from django.contrib.contenttypes.models import ContentType
       from sample.models import Continent
       from translations.utils import get_translations
       from translations.utils import get_translations_dictionary
       from translations.utils import apply_obj_translations

       europe = Continent.objects.get(code="EU")
       translations = get_translations(europe, lang="de")
       dictionary = get_translations_dictionary(translations)
       europe_ct = ContentType.objects.get_for_model(europe)
       ct_dictionary = dictionary[europe_ct.id]

       apply_obj_translations(europe, ct_dictionary, included=True)

       print(europe)

    .. testoutput:: apply_obj_translations

       Europa
    """
    if included and ct_dictionary:
        try:
            fields = ct_dictionary[str(obj.id)]
        except KeyError:
            pass
        else:
            for (field, text) in fields.items():
                setattr(obj, field, text)


def apply_rel_translations(obj, hierarchy, dictionary):
    """
    Apply translations dictionary on a relations hierarchy of an object.

    Loops through the :term:`relations hierarchy` of an object, Searches
    the :term:`translations dictionary` for the translations of the relation
    and applies them on the relation, field by field and in place.

    :param obj: The object to apply the translations dictionary on the
        relations hierarchy of it.
    :type obj: ~django.db.models.Model
    :param hierarchy: The relations hierarchy to apply the translations
        dictionary on.
    :type hierarchy: dict(str, dict)
    :param dictionary: The translations dictionary to use for the translation
        process.
    :type dictionary: dict(int, dict(str, dict(str, str)))

    .. testsetup:: apply_rel_translations

       from tests.sample import create_samples

       create_samples(
           continent_names=["europe"],
           country_names=["germany"]
           continent_fields=["name", "denonym"],
           country_fields=["name", "denonym"],
           langs=["de"]
       )

    To apply the translations dictionary on a relations hierarchy of an
    object:

    .. testcode:: apply_rel_translations

       from sample.models import Continent
       from translations.utils import get_translations
       from translations.utils import get_translations_dictionary
       from translations.utils import get_relations_hierarchy
       from translations.utils import apply_rel_translations

       europe = Continent.objects.prefetch_related(
           'countries'
       ).get(code="EU")
       translations = get_translations(europe, 'countries', lang="de")
       dictionary = get_translations_dictionary(translations)
       hierarchy = get_relations_hierarchy('countries')

       apply_rel_translations(europe, hierarchy, dictionary)

       print(europe.countries.all())

    .. testoutput:: apply_rel_translations

       Europa
    """
    if hierarchy:
        for (relation, detail) in hierarchy.items():
            value = getattr(obj, relation, None)
            if value is not None:
                if isinstance(value, models.Manager):
                    value = value.all()
                translate(
                    value,
                    detail['relations'],
                    dictionary,
                    included=detail['included']
                )


def translate(entity, hierarchy, dictionary, included=True):
    model, iterable = get_entity_details(entity)

    if model is None:
        return

    content_type = ContentType.objects.get_for_model(model)
    ct_dictionary = dictionary[content_type.id]

    if iterable:
        for obj in entity:
            apply_obj_translations(obj, ct_dictionary, included=included)
            apply_rel_translations(obj, hierarchy, dictionary)
    else:
        apply_obj_translations(entity, ct_dictionary, included=included)
        apply_rel_translations(entity, hierarchy, dictionary)


def read_translations(entity, *relations, lang=None):
    """
    Translate an entity and the relations of it in a language.

    Translates the entity and the relations of it in a language or using a
    :term:`translations dictionary`. If the translations dictionary isn't
    provided it makes a translations dictionary automatically out of the
    translations of the entity and the relations of it in a language then
    apply that for the translation process, otherwise it just uses the
    provided translations dictionary.

    :param entity: The entity to translate.
    :type entity: ~django.db.models.Model or
        ~collections.Iterable(~django.db.models.Model)
    :param relations: The relations of the entity to translate.
    :type relations: list(str)
    :param lang: The language to translate in.
        ``None`` means use the active language code. [#active_language]_
    :type lang: str or None
    :param dictionary: The translations dictionary to use for the translation
        process.
        ``None`` means create the translations dictionary automatically.
    :type dictionary: dict(int, dict(str, dict(str, str))) or None
    :param included: Whether the entity itself should be translated along
        with the relations of it or not, the default is ``True``.
    :type included: bool
    :raise ValueError: If the language code is not included in
        the :data:`~django.conf.settings.LANGUAGES` setting.
    :raise TypeError: If the entity is neither a model instance nor
        an iterable of model instances.
    :raise ~django.core.exceptions.FieldDoesNotExist: If a relation is
        pointing to the fields that don't exist.

    .. testsetup:: read_translations

       from tests.sample import create_samples

       create_samples(
           continent_names=["europe", "asia"],
           country_names=["germany", "south korea"],
           city_names=["cologne", "munich", "seoul", "ulsan"],
           continent_fields=["name", "denonym"],
           country_fields=["name", "denonym"],
           city_fields=["name", "denonym"],
           langs=["de"]
       )

    To translate a list of model instances:

    .. testcode:: read_translations

       from sample.models import Continent, Country, City
       from translations.utils import read_translations

       continents = list(Continent.objects.all())

       read_translations(continents, lang="de")

       print(continents)

    .. testoutput:: read_translations

       [<Continent: Europa>, <Continent: Asien>]

    To translate a queryset:

    .. testcode:: read_translations

       from sample.models import Continent, Country, City
       from translations.utils import read_translations

       continents = Continent.objects.all()

       read_translations(continents, lang="de")

       print(continents)

    .. testoutput:: read_translations

       <TranslatableQuerySet [<Continent: Europa>, <Continent: Asien>]>

    To translate a model instance:

    .. testcode:: read_translations

       from sample.models import Continent, Country, City
       from translations.utils import read_translations

       europe = Continent.objects.get(code="EU")

       read_translations(europe, lang="de")

       print(europe)

    .. testoutput:: read_translations

       Europa

    .. warning::
       Always use :meth:`~django.db.models.query.QuerySet.select_related`,
       :meth:`~django.db.models.query.QuerySet.prefetch_related` or
       :func:`~django.db.models.prefetch_related_objects` for fetching the
       relations of the entity before using :func:`read_translations` on it.

       Instead of:

       .. testcode:: read_translations

          from sample.models import Continent, Country, City
          from translations.utils import read_translations

          # Not using `prefetch_related`
          continents = Continent.objects.all()

          read_translations(continents, "countries", "countries__cities", lang="de")

          for continent in continents:
              print("Continent: {}".format(continent))
              for country in continent.countries.all():
                  print("Country: {} # Wrong".format(country))
                  for city in country.cities.all():
                      print("City: {} # Wrong".format(city))

       .. testoutput:: read_translations

          Continent: Europa
          Country: Germany # Wrong
          City: Cologne # Wrong
          City: Munich # Wrong
          Continent: Asien
          Country: South Korea # Wrong
          City: Seoul # Wrong
          City: Ulsan # Wrong

       This must be done:

       .. testcode:: read_translations

          from sample.models import Continent, Country, City
          from translations.utils import read_translations

          # Using `prefetch_related`
          continents = Continent.objects.prefetch_related(
              'countries', 'countries__cities'
          ).all()

          read_translations(continents, "countries", "countries__cities", lang="de")

          for continent in continents:
              print("Continent: {}".format(continent))
              for country in continent.countries.all():
                  print("Country: {} # Correct".format(country))
                  for city in country.cities.all():
                      print("City: {} # Correct".format(city))

       .. testoutput:: read_translations

          Continent: Europa
          Country: Deutschland # Correct
          City: Köln # Correct
          City: München # Correct
          Continent: Asien
          Country: Südkorea # Correct
          City: Seül # Correct
          City: Ulsän # Correct

    To translate a list of model instances with relations:

    .. testcode:: read_translations

       from django.db.models import prefetch_related_objects
       from sample.models import Continent, Country, City
       from translations.utils import read_translations

       continents = list(Continent.objects.all())
       prefetch_related_objects(continents, 'countries', 'countries__cities')

       read_translations(continents, "countries", "countries__cities", lang="de")

       for continent in continents:
           print("Continent: {}".format(continent))
           for country in continent.countries.all():
               print("Country: {}".format(country))
               for city in country.cities.all():
                   print("City: {}".format(city))

    .. testoutput:: read_translations

       Continent: Europa
       Country: Deutschland
       City: Köln
       City: München
       Continent: Asien
       Country: Südkorea
       City: Seül
       City: Ulsän

    To translate a queryset with relations:

    .. testcode:: read_translations

       from sample.models import Continent, Country, City
       from translations.utils import read_translations

       continents = Continent.objects.prefetch_related(
           'countries', 'countries__cities'
       ).all()

       read_translations(continents, "countries", "countries__cities", lang="de")

       for continent in continents:
           print("Continent: {}".format(continent))
           for country in continent.countries.all():
               print("Country: {}".format(country))
               for city in country.cities.all():
                   print("City: {}".format(city))

    .. testoutput:: read_translations

       Continent: Europa
       Country: Deutschland
       City: Köln
       City: München
       Continent: Asien
       Country: Südkorea
       City: Seül
       City: Ulsän

    To translate a model instance with relations:

    .. testcode:: read_translations

       from django.db.models import prefetch_related_objects
       from sample.models import Continent, Country, City
       from translations.utils import read_translations

       europe = Continent.objects.get(code="EU")
       prefetch_related_objects([europe], 'countries', 'countries__cities')

       read_translations(europe, "countries", "countries__cities", lang="de")

       print("Continent: {}".format(europe))
       for country in europe.countries.all():
           print("Country: {}".format(country))
           for city in country.cities.all():
               print("City: {}".format(city))

    .. testoutput:: read_translations

       Continent: Europa
       Country: Deutschland
       City: Köln
       City: München

    .. warning::
       If the relations of an entity must be filtered along the way, do it
       before using :func:`read_translations` on it.

       Instead of:

       .. testcode:: read_translations

          from sample.models import Continent, Country, City
          from translations.utils import read_translations

          # Not using `Prefetch`
          continents = Continent.objects.prefetch_related(
              'countries', 'countries__cities'
          ).all()

          read_translations(continents, "countries", "countries__cities", lang="de")

          for continent in continents:
              print("Continent: {}".format(continent))
              for country in continent.countries.filter(code__isnull=False):
                  print("Country: {} # Wrong".format(country))
                  for city in country.cities.all():
                      print("City: {} # Wrong".format(city))

       .. testoutput:: read_translations

          Continent: Europa
          Country: Germany # Wrong
          City: Cologne # Wrong
          City: Munich # Wrong
          Continent: Asien
          Country: South Korea # Wrong
          City: Seoul # Wrong
          City: Ulsan # Wrong

       This must be done:

       .. testcode:: read_translations

          from django.db.models import Prefetch
          from sample.models import Continent, Country, City
          from translations.utils import read_translations

          # Using `Prefetch`
          continents = Continent.objects.prefetch_related(
              Prefetch(
                  'countries',
                  queryset=Country.objects.filter(code__isnull=False)
              ),
              'countries__cities'
          ).all()

          read_translations(continents, "countries", "countries__cities", lang="de")

          for continent in continents:
              print("Continent: {}".format(continent))
              for country in continent.countries.all():
                  print("Country: {} # Correct".format(country))
                  for city in country.cities.all():
                      print("City: {} # Correct".format(city))

       .. testoutput:: read_translations

          Continent: Europa
          Country: Deutschland # Correct
          City: Köln # Correct
          City: München # Correct
          Continent: Asien
          Country: Südkorea # Correct
          City: Seül # Correct
          City: Ulsän # Correct
    """
    hierarchy = get_relations_hierarchy(*relations)

    dictionary = get_translations_dictionary(
        get_translations(
            entity,
            *relations,
            lang=lang
        )
    )

    translate(entity, hierarchy, dictionary, included=True)


def update_translations(entity, lang=None):
    lang = get_translation_language(lang)
    model, iterable = get_entity_details(entity)

    # ------------ renew transaction
    if issubclass(model, translations.models.Translatable):
        translatable_fields = model.get_translatable_fields()
        try:
            with transaction.atomic():
                # ------------ delete old translations
                translations_queryset = get_translations(
                    entity,
                    lang=lang
                )
                translations_queryset.select_for_update().delete()

                # ------------ add new translations
                translations_objects = []

                # add translations function
                def add_translations(obj):
                    for field in translatable_fields:
                        field_value = getattr(obj, field.name, None)
                        if field_value:
                            translations_objects.append(
                                translations.models.Translation(
                                    content_object=obj,
                                    language=lang,
                                    field=field.name,
                                    text=field_value
                                )
                            )

                # translate based on plural/singular
                if iterable:
                    for obj in entity:
                        add_translations(obj)
                else:
                    add_translations(entity)

                if len(translations_objects) > 0:
                    translations.models.Translation.objects.bulk_create(translations_objects)
        except Exception:
            raise
