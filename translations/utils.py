"""
This module contains the utilities for the Translations app.

.. rubric:: Functions:

:func:`_get_translation_language`
    Return a language code to use in the translation process.
:func:`_get_entity_details`
    Return the iteration and type details of an entity.
:func:`_get_reverse_relation`
    Return the reverse of a model's relation.
:func:`_get_translations_reverse_relation`
    Return the reverse of a model's translations relation or the translations
    relation of a model's relation.
:func:`_get_translations`
    Return the translations of an entity and the relations of it in a language.
:func:`_get_translations_dictionary`
    Return the :term:`translations dictionary` made out of some translations.
:func:`_fill_hierarchy`
    Fills a :term:`relations hierarchy` with parts of a relation.
:func:`_get_relations_hierarchy`
    Return the :term:`relations hierarchy` made out of some relations.
:func:`_apply_obj_translations`
    Apply a :term:`content type translations dictionary` on an object.
:func:`_apply_rel_translations`
    Apply a :term:`translations dictionary` on a :term:`relations hierarchy`
    of an object.
:func:`_apply_entity_translations`
    Apply a :term:`translations dictionary` on an entity and a
    :term:`relations hierarchy` of it.
:func:`apply_translations`
    Apply the translations on an entity and the relations of it in a language.
"""

from django.db import models, transaction
from django.db.models.constants import LOOKUP_SEP
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import get_language
from django.conf import settings

import translations.models


__docformat__ = 'restructuredtext'


def _get_translation_language(lang=None):
    """
    Return a language code to use in the translation process.

    If the custom language code is passed in it returns the custom language
    code, otherwise it returns the :term:`active language` code.

    :param lang: The custom language code to use in the translation process.
        ``None`` means use the :term:`active language` code.
    :type lang: str or None
    :return: The language code to use in the translation process.
    :rtype: str
    :raise ValueError: If the language code is not specified in
        the :data:`~django.conf.settings.LANGUAGES` setting.

    .. testsetup:: _get_translation_language

       from django.utils.translation import activate

       activate('en')

    To get the :term:`active language` code:

    .. testcode:: _get_translation_language

       from translations.utils import _get_translation_language

       active = _get_translation_language()
       print("Language code: {}".format(active))

    .. testoutput:: _get_translation_language

       Language code: en

    To get a custom language code:

    .. testcode:: _get_translation_language

       from translations.utils import _get_translation_language

       custom = _get_translation_language('de')
       print("Language code: {}".format(custom))

    .. testoutput:: _get_translation_language

       Language code: de
    """
    lang = lang if lang else get_language()

    if lang not in [language[0] for language in settings.LANGUAGES]:
        raise ValueError(
            "The language code `{}` is not supported.".format(lang)
        )

    return lang


def _get_entity_details(entity):
    """
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
       even if the iterable is an empty queryset (which its model can be
       retrieved). It's because the other parts of the code first check to see
       if the model in the details is ``None``, in that case they skip the
       translation process all together (because there's nothing to
       translate).

    .. testsetup:: _get_entity_details

       from tests.sample import create_samples

       create_samples(continent_names=["europe"])

    To get the details of a list of instances:

    .. testcode:: _get_entity_details

       from sample.models import Continent
       from translations.utils import _get_entity_details

       continents = list(Continent.objects.all())
       details = _get_entity_details(continents)
       print("Iterable: {}".format(details[0]))
       print("Model: {}".format(details[1]))

    .. testoutput:: _get_entity_details

       Iterable: True
       Model: <class 'sample.models.Continent'>

    To get the details of a queryset:

    .. testcode:: _get_entity_details

       from sample.models import Continent
       from translations.utils import _get_entity_details

       continents = Continent.objects.all()
       details = _get_entity_details(continents)
       print("Iterable: {}".format(details[0]))
       print("Model: {}".format(details[1]))

    .. testoutput:: _get_entity_details

       Iterable: True
       Model: <class 'sample.models.Continent'>

    To get the details of an instance:

    .. testcode:: _get_entity_details

       from sample.models import Continent
       from translations.utils import _get_entity_details

       europe = Continent.objects.get(code="EU")
       details = _get_entity_details(europe)
       print("Iterable: {}".format(details[0]))
       print("Model: {}".format(details[1]))

    .. testoutput:: _get_entity_details

       Iterable: False
       Model: <class 'sample.models.Continent'>

    To get the details of an empty list:

    .. testcode:: _get_entity_details

       from sample.models import Continent
       from translations.utils import _get_entity_details

       empty = []
       details = _get_entity_details(empty)
       print("Iterable: {}".format(details[0]))
       print("Model: {}".format(details[1]))

    .. testoutput:: _get_entity_details

       Iterable: True
       Model: None
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

    return (iterable, model)


def _get_reverse_relation(model, relation):
    """
    Return the reverse of a model's relation.

    Processes the model's relation which points from the model to the target
    model and returns the reverse relation which points from the target model
    to the model.

    :param model: The model which contains the relation and the reverse
        relation points to.
    :type model: type(~django.db.models.Model)
    :param relation: The relation of the model to get the reverse of.
        It may be composed of many ``related_query_name``\\ s separated by
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

       reverse_relation = _get_reverse_relation(Continent, 'countries__cities')
       print("City can be queried with '{}'".format(reverse_relation))

    .. testoutput:: _get_reverse_relation

       City can be queried with 'country__continent'
    """
    parts = relation.split(LOOKUP_SEP)
    root = parts[0]
    branch = parts[1:]

    field = model._meta.get_field(root)
    reverse_relation = field.remote_field.name

    if branch:
        branch_model = field.related_model
        branch_relation = LOOKUP_SEP.join(branch)
        branch_reverse_relation = _get_reverse_relation(
            branch_model,
            branch_relation
        )
        return '{}__{}'.format(
            branch_reverse_relation,
            reverse_relation
        )
    else:
        return reverse_relation


def _get_translations_reverse_relation(model, relation=None):
    """
    Return the reverse of a model's translations relation or the translations
    relation of a model's relation.

    If the relation is not passed in, it processes the model's translations
    relation which points from the model to the
    :class:`~translations.models.Translation` model directly and returns the
    reverse relation which points from the
    :class:`~translations.models.Translation` model to the model directly,
    otherwise it processes the translations relation of the model's relation
    which points from the model to the
    :class:`~translations.models.Translation` model indirectly (through the
    relation) and returns the reverse relation which points from the
    :class:`~translations.models.Translation` model to the model indirectly
    (through the reverse relation).

    :param model: The model which contains the translations relation directly
        or indirectly (either it contains the translations relation itself, or
        the specified relation contains it) and which the reverse relation
        points to.
    :type model: type(~django.db.models.Model)
    :param relation: The relation of the model to get the translations
        relation's reverse of.
        It may be composed of many ``related_query_name``\\ s separated by
        :data:`~django.db.models.constants.LOOKUP_SEP` (usually ``__``) to
        represent a deeply nested relation.
        ``None`` means the reverse relation of the model's translations
        relation should be returned.
    :type relation: str or None
    :return: The reverse of the model’s translations relation or the
        translations relation of the model’s relation.
    :rtype: str
    :raise ~django.core.exceptions.FieldDoesNotExist: If the relation is
        pointing to the fields that don't exist.

    To get the reverse of the translations relation of a model's relation:

    .. testcode:: _get_translations_reverse_relation

       from sample.models import Continent
       from translations.utils import _get_translations_reverse_relation

       reverse_relation = _get_translations_reverse_relation(
           Continent, 'countries__cities')
       print("Translation can be queried with '{}'".format(reverse_relation))

    .. testoutput:: _get_translations_reverse_relation

       Translation can be queried with 'sample_city__country__continent'

    To get the reverse of a model's translations relation:

    .. testcode:: _get_translations_reverse_relation

       from sample.models import Continent
       from translations.utils import _get_translations_reverse_relation

       reverse_relation = _get_translations_reverse_relation(Continent)
       print("Translation can be queried with '{}'".format(reverse_relation))

    .. testoutput:: _get_translations_reverse_relation

       Translation can be queried with 'sample_continent'
    """
    if relation is None:
        translations_relation = 'translations'
    else:
        translations_relation = '{}__{}'.format(relation, 'translations')

    return _get_reverse_relation(model, translations_relation)


def _get_translations(entity, *relations, lang=None):
    """
    Return the translations of an entity and the relations of it in a language.

    Fetches the translations of the entity and the specified relations of it
    in a language and returns them as a
    :class:`~translations.models.Translation` queryset.

    :param entity: The entity to fetch the translations of.
    :type entity: ~django.db.models.Model or
        ~collections.Iterable(~django.db.models.Model)
    :param relations: The relations of the entity to fetch the
        translations of.
    :type relations: list(str)
    :param lang: The language to fetch the translations in.
        ``None`` means use the :term:`active language` code.
    :type lang: str or None
    :return: The translations.
    :rtype: ~django.db.models.query.QuerySet(~translations.models.Translation)
    :raise ValueError: If the language code is not included in
        the :data:`~django.conf.settings.LANGUAGES` setting.
    :raise TypeError: If the entity is neither a model instance nor
        an iterable of model instances.
    :raise ~django.core.exceptions.FieldDoesNotExist: If a relation is
        pointing to the fields that don't exist.

    .. testsetup:: _get_translations

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

    To get the translations of a list of instances and the relations of them:

    .. testcode:: _get_translations

       from sample.models import Continent
       from translations.utils import _get_translations

       continents = list(Continent.objects.all())

       translations = _get_translations(
           continents,
           "countries", "countries__cities",
           lang="de"
       )

       print(translations)

    .. testoutput:: _get_translations

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
           <Translation: Seouler: Seüler>,
           <Translation: Ulsan: Ulsän>,
           <Translation: Ulsanian: Ulsänisch>
       ]>

    To get the translations of a queryset and the relations of it:

    .. testcode:: _get_translations

       from sample.models import Continent
       from translations.utils import _get_translations

       continents = Continent.objects.all()

       translations = _get_translations(
           continents,
           "countries", "countries__cities",
           lang="de"
       )

       print(translations)

    .. testoutput:: _get_translations

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
           <Translation: Seouler: Seüler>,
           <Translation: Ulsan: Ulsän>,
           <Translation: Ulsanian: Ulsänisch>
       ]>

    To get the translations of an instance and the relations of it:

    .. testcode:: _get_translations

       from sample.models import Continent
       from translations.utils import _get_translations

       europe = Continent.objects.get(code="EU")

       translations = _get_translations(
           europe,
           "countries", "countries__cities",
           lang="de"
       )

       print(translations)

    .. testoutput:: _get_translations

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
    lang = _get_translation_language(lang)
    iterable, model = _get_entity_details(entity)

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
        trans = _get_translations_reverse_relation(model)
        prop = '{}__{}'.format(trans, condition)
        queries.append(
            models.Q(**{prop: value})
        )

    for relation in relations:
        trans = _get_translations_reverse_relation(model, relation)
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


def _get_translations_dictionary(translations):
    """
    Return the :term:`translations dictionary` made out of some translations.

    Processes the translations and returns the :term:`translations dictionary`
    to use in the translation process.

    :param translations: The translations to make
        the :term:`translations dictionary` out of.
    :type translations: ~django.db.models.query.QuerySet(\\
        ~translations.models.Translation)
    :return: The :term:`translations dictionary` made out of translations.
    :rtype: dict(int, dict(str, dict(str, str)))

    .. warning::
       The translations **must** be filtered in a language before being passed
       in, otherwise the :term:`translations dictionary` may end up being a
       mix of several languages.

    .. testsetup:: _get_translations_dictionary

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

    To get the :term:`translations dictionary` of the german translations.

    .. testcode:: _get_translations_dictionary

       from django.contrib.contenttypes.models import ContentType
       from sample.models import Continent, Country, City
       from translations.utils import _get_translations_dictionary
       from translations.models import Translation

       translations = Translation.objects.filter(language="de")
       dictionary = _get_translations_dictionary(translations)

       continent_ct = ContentType.objects.get_for_model(Continent).id
       continent_translations = list(dictionary[continent_ct].items())
       continent_translations.sort(key=lambda x: x[0])
       print("Continent translations:")
       for id, translation in continent_translations:
           print(translation)

       country_ct = ContentType.objects.get_for_model(Country).id
       country_translations = list(dictionary[country_ct].items())
       country_translations.sort(key=lambda x: x[0])
       print("Country translations:")
       for id, translation in country_translations:
           print(translation)

       city_ct = ContentType.objects.get_for_model(City).id
       city_translations = list(dictionary[city_ct].items())
       city_translations.sort(key=lambda x: x[0])
       print("City translations:")
       for id, translation in city_translations:
           print(translation)

    .. testoutput:: _get_translations_dictionary

       Continent translations:
       {'denonym': 'Europäisch', 'name': 'Europa'}
       {'denonym': 'Asiatisch', 'name': 'Asien'}
       Country translations:
       {'denonym': 'Deutsche', 'name': 'Deutschland'}
       {'denonym': 'Südkoreanisch', 'name': 'Südkorea'}
       City translations:
       {'denonym': 'Kölner', 'name': 'Köln'}
       {'denonym': 'Münchner', 'name': 'München'}
       {'denonym': 'Seüler', 'name': 'Seül'}
       {'denonym': 'Ulsänisch', 'name': 'Ulsän'}
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


def _fill_hierarchy(hierarchy, *relation_parts):
    """
    Fills a :term:`relations hierarchy` with parts of a relation.

    Fills the :term:`relations hierarchy` based on the order of the relation
    parts. The later parts are considered as the children of the earlier ones.
    The last part is considered included.

    :param hierarchy: The :term:`relations hierarchy` to fill.
    :type hierarchy: dict(str, dict)
    :param relation_parts: The parts of the relation to fill the
        :term:`relations hierarchy` with.
    :type relation_parts: list(str)

    To fill the :term:`relations hierarchy` with one level of relation parts:

    .. testcode:: _fill_hierarchy

       from translations.utils import _fill_hierarchy

       hierarchy = {}

       _fill_hierarchy(hierarchy, 'countries')

       print(hierarchy)

    .. testoutput:: _fill_hierarchy

       {'countries': {'included': True, 'relations': {}}}

    To fill the :term:`relations hierarchy` with two level of relation parts,
    not including the first one:

    .. testcode:: _fill_hierarchy

       from translations.utils import _fill_hierarchy

       hierarchy = {}

       _fill_hierarchy(hierarchy, 'countries', 'cities')

       print(hierarchy)

    .. testoutput:: _fill_hierarchy

       {'countries': {'included': False,
                      'relations': {'cities': {'included': True,
                                               'relations': {}}}}}

    To fill the :term:`relations hierarchy` with two level of relation parts,
    including the first one:

    .. testcode:: _fill_hierarchy

       from translations.utils import _fill_hierarchy

       hierarchy = {}

       _fill_hierarchy(hierarchy, 'countries')
       _fill_hierarchy(hierarchy, 'countries', 'cities')

       print(hierarchy)

    .. testoutput:: _fill_hierarchy

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
        _fill_hierarchy(hierarchy[root]["relations"], *nest)
    else:
        hierarchy[root]["included"] = True


def _get_relations_hierarchy(*relations):
    """
    Return the :term:`relations hierarchy` made out of some relations.

    Processes the relations and returns the :term:`relations hierarchy` to
    use in the translation process.

    :param relations: The relations to make the :term:`relations hierarchy`
        out of.
    :type relations: list(str)
    :return: The :term:`relations hierarchy` made out of relations.
    :rtype: dict(str, dict)

    To get the :term:`relations hierarchy` of a first-level relation:

    .. testcode::

       from translations.utils import _get_relations_hierarchy

       print(_get_relations_hierarchy('countries'))

    .. testoutput::

       {'countries': {'included': True, 'relations': {}}}

    To get the :term:`relations hierarchy` of a second-level relation,
    not including the first-level relation:

    .. testcode::

       from translations.utils import _get_relations_hierarchy

       print(_get_relations_hierarchy('countries__cities'))

    .. testoutput::

       {'countries': {'included': False,
                      'relations': {'cities': {'included': True,
                                               'relations': {}}}}}

    To get the :term:`relations hierarchy` of a second-level relation,
    including the first-level relation:

    .. testcode::

       from translations.utils import _get_relations_hierarchy

       print(_get_relations_hierarchy('countries', 'countries__cities'))

    .. testoutput::

       {'countries': {'included': True,
                      'relations': {'cities': {'included': True,
                                               'relations': {}}}}}

    To get the :term:`relations hierarchy` of no relations:

    .. testcode::

       from translations.utils import _get_relations_hierarchy

       print(_get_relations_hierarchy())

    .. testoutput::

       {}
    """
    hierarchy = {}
    for relation in relations:
        parts = relation.split(LOOKUP_SEP)
        _fill_hierarchy(hierarchy, *parts)
    return hierarchy


def _apply_obj_translations(obj, ct_dictionary, included=True):
    """
    Apply a :term:`content type translations dictionary` on an object.

    Searches the :term:`content type translations dictionary` for the
    translations of the object and applies them on the object, field by field
    and in place.

    :param obj: The object to apply
        the :term:`content type translations dictionary` on.
    :type obj: ~django.db.models.Model
    :param ct_dictionary: The :term:`content type translations dictionary` to
        be applied on the object.
    :type ct_dictionary: dict(str, dict(str, str))
    :param included: Whether to apply
        the :term:`content type translations dictionary` on the object or not.
    :type included: bool

    .. testsetup:: _apply_obj_translations

       from tests.sample import create_samples

       create_samples(
           continent_names=["europe"],
           continent_fields=["name", "denonym"],
           langs=["de"]
       )

    To apply the :term:`content type translations dictionary` on an object:

    .. testcode:: _apply_obj_translations

       from django.contrib.contenttypes.models import ContentType
       from sample.models import Continent
       from translations.utils import _get_translations
       from translations.utils import _get_translations_dictionary
       from translations.utils import _apply_obj_translations

       europe = Continent.objects.get(code="EU")
       translations = _get_translations(europe, lang="de")
       dictionary = _get_translations_dictionary(translations)
       europe_ct = ContentType.objects.get_for_model(europe)
       ct_dictionary = dictionary[europe_ct.id]

       _apply_obj_translations(europe, ct_dictionary, included=True)

       print(europe)

    .. testoutput:: _apply_obj_translations

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


def _apply_rel_translations(obj, hierarchy, dictionary):
    """
    Apply a :term:`translations dictionary` on a :term:`relations hierarchy`
    of an object.

    Searches the :term:`translations dictionary` for the translations of the
    object's :term:`relations hierarchy` and applies them, field by field
    and in place.

    :param obj: The object to apply the :term:`translations dictionary` on the
        :term:`relations hierarchy` of.
    :type obj: ~django.db.models.Model
    :param hierarchy: The :term:`relations hierarchy` of the object to apply
        the :term:`translations dictionary` on.
    :type hierarchy: dict(str, dict)
    :param dictionary: The :term:`translations dictionary` to apply on the
        :term:`relations hierarchy` of the object.
    :type dictionary: dict(int, dict(str, dict(str, str)))

    .. warning::
       The relations of an instance, a queryset or a list of instances
       **must** be fetched before performing the translation process.

       To do this use :meth:`~django.db.models.query.QuerySet.select_related`,
       :meth:`~django.db.models.query.QuerySet.prefetch_related` or
       :func:`~django.db.models.prefetch_related_objects`.

    .. warning::
       Only when all the filterings are executed on the relations of an
       instance, a queryset or a list of instances, they should go through the
       translation process, otherwise if a relation is filtered after the
       translation process the translations of that relation are reset.

       To filter a relation when fetching it use
       :class:`~django.db.models.Prefetch`.

    .. testsetup:: _apply_rel_translations

       from tests.sample import create_samples

       create_samples(
           continent_names=["europe"],
           country_names=["germany"],
           continent_fields=["name", "denonym"],
           country_fields=["name", "denonym"],
           langs=["de"]
       )

    To apply a :term:`translations dictionary` on a
    :term:`relations hierarchy` of an object:

    .. testcode:: _apply_rel_translations

       from sample.models import Continent
       from translations.utils import _get_translations
       from translations.utils import _get_translations_dictionary
       from translations.utils import _get_relations_hierarchy
       from translations.utils import _apply_rel_translations

       relations = ('countries',)

       europe = Continent.objects.prefetch_related(*relations).get(code="EU")

       translations = _get_translations(europe, *relations, lang="de")
       dictionary = _get_translations_dictionary(translations)
       hierarchy = _get_relations_hierarchy(*relations)

       _apply_rel_translations(europe, hierarchy, dictionary)

       print(europe.countries.all())

    .. testoutput:: _apply_rel_translations

       <TranslatableQuerySet [<Country: Deutschland>]>
    """
    if hierarchy:
        for (relation, detail) in hierarchy.items():
            value = getattr(obj, relation, None)
            if value is not None:
                if isinstance(value, models.Manager):
                    value = value.all()
                _apply_entity_translations(
                    value,
                    detail['relations'],
                    dictionary,
                    included=detail['included']
                )


def _apply_entity_translations(entity, hierarchy, dictionary, included=True):
    """
    Apply a :term:`translations dictionary` on an entity and a
    :term:`relations hierarchy` of it.

    Searches the :term:`translations dictionary` for the translations of the
    entity and the :term:`relations hierarchy` of it and applies them, field
    by field and in place.

    :param entity: The entity to apply the :term:`translations dictionary` on
        and on the :term:`relations hierarchy` of.
    :type entity: ~django.db.models.Model or
        ~collections.Iterable(~django.db.models.Model)
    :param hierarchy: The :term:`relations hierarchy` of the entity to apply
        the :term:`translations dictionary` on.
    :type hierarchy: dict(str, dict)
    :param dictionary: The :term:`translations dictionary` to apply on the
        entity and on the :term:`relations hierarchy` of it.
    :type dictionary: dict(int, dict(str, dict(str, str)))
    :param included: Whether to apply the :term:`translations dictionary` on
        the entity or not.
    :type included: bool
    :raise TypeError: If the entity is neither a model instance nor
        an iterable of model instances.

    .. warning::
       The relations of an instance, a queryset or a list of instances
       **must** be fetched before performing the translation process.

       To do this use :meth:`~django.db.models.query.QuerySet.select_related`,
       :meth:`~django.db.models.query.QuerySet.prefetch_related` or
       :func:`~django.db.models.prefetch_related_objects`.

    .. warning::
       Only when all the filterings are executed on the relations of an
       instance, a queryset or a list of instances, they should go through the
       translation process, otherwise if a relation is filtered after the
       translation process the translations of that relation are reset.

       To filter a relation when fetching it use
       :class:`~django.db.models.Prefetch`.

    .. testsetup:: _apply_entity_translations

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

    To apply a :term:`translations dictionary` on a list of instances and a
    :term:`relations hierarchy` of it:

    .. testcode:: _apply_entity_translations

       from django.db.models import prefetch_related_objects
       from sample.models import Continent
       from translations.utils import _get_translations
       from translations.utils import _get_translations_dictionary
       from translations.utils import _get_relations_hierarchy
       from translations.utils import _apply_entity_translations

       relations = ('countries', 'countries__cities',)

       continents = list(Continent.objects.all())
       prefetch_related_objects(continents, *relations)

       translations = _get_translations(continents, *relations, lang="de")
       dictionary = _get_translations_dictionary(translations)
       hierarchy = _get_relations_hierarchy(*relations)

       _apply_entity_translations(continents, hierarchy, dictionary)

       for continent in continents:
           print("Continent: {}".format(continent))
           for country in continent.countries.all():
               print("Country: {}".format(country))
               for city in country.cities.all():
                   print("City: {}".format(city))

    .. testoutput:: _apply_entity_translations

       Continent: Europa
       Country: Deutschland
       City: Köln
       City: München
       Continent: Asien
       Country: Südkorea
       City: Seül
       City: Ulsän

    To apply a :term:`translations dictionary` on a queryset and a
    :term:`relations hierarchy` of it:

    .. testcode:: _apply_entity_translations

       from sample.models import Continent
       from translations.utils import _get_translations
       from translations.utils import _get_translations_dictionary
       from translations.utils import _get_relations_hierarchy
       from translations.utils import _apply_entity_translations

       relations = ('countries', 'countries__cities',)

       continents = Continent.objects.prefetch_related(*relations).all()

       translations = _get_translations(continents, *relations, lang="de")
       dictionary = _get_translations_dictionary(translations)
       hierarchy = _get_relations_hierarchy(*relations)

       _apply_entity_translations(continents, hierarchy, dictionary)

       for continent in continents:
           print("Continent: {}".format(continent))
           for country in continent.countries.all():
               print("Country: {}".format(country))
               for city in country.cities.all():
                   print("City: {}".format(city))

    .. testoutput:: _apply_entity_translations

       Continent: Europa
       Country: Deutschland
       City: Köln
       City: München
       Continent: Asien
       Country: Südkorea
       City: Seül
       City: Ulsän

    To apply a :term:`translations dictionary` on an instance and a
    :term:`relations hierarchy` of it:

    .. testcode:: _apply_entity_translations

       from django.db.models import prefetch_related_objects
       from sample.models import Continent
       from translations.utils import _get_translations
       from translations.utils import _get_translations_dictionary
       from translations.utils import _get_relations_hierarchy
       from translations.utils import _apply_entity_translations

       relations = ('countries', 'countries__cities',)

       europe = Continent.objects.get(code="EU")
       prefetch_related_objects([europe], *relations)

       translations = _get_translations(europe, *relations, lang="de")
       dictionary = _get_translations_dictionary(translations)
       hierarchy = _get_relations_hierarchy(*relations)

       _apply_entity_translations(europe, hierarchy, dictionary)

       print("Continent: {}".format(europe))
       for country in europe.countries.all():
           print("Country: {}".format(country))
           for city in country.cities.all():
               print("City: {}".format(city))

    .. testoutput:: _apply_entity_translations

       Continent: Europa
       Country: Deutschland
       City: Köln
       City: München
    """
    iterable, model = _get_entity_details(entity)

    if model is None:
        return

    content_type = ContentType.objects.get_for_model(model)
    ct_dictionary = dictionary.get(content_type.id, {})

    if iterable:
        for obj in entity:
            _apply_obj_translations(obj, ct_dictionary, included=included)
            _apply_rel_translations(obj, hierarchy, dictionary)
    else:
        _apply_obj_translations(entity, ct_dictionary, included=included)
        _apply_rel_translations(entity, hierarchy, dictionary)


def apply_translations(entity, *relations, lang=None):
    """
    Apply the translations on an entity and the relations of it in a language.

    Fetches the translations of the entity and the specified relations of it
    in a language and applies them, field by field and in place.

    :param entity: The entity to apply the translations on and on the
        relations of.
    :type entity: ~django.db.models.Model or
        ~collections.Iterable(~django.db.models.Model)
    :param relations: The relations of the entity to apply the translations
        on.
    :type relations: list(str)
    :param lang: The language to fetch the translations in.
        ``None`` means use the :term:`active language` code.
    :type lang: str or None
    :raise ValueError: If the language code is not included in
        the :data:`~django.conf.settings.LANGUAGES` setting.
    :raise TypeError: If the entity is neither a model instance nor
        an iterable of model instances.
    :raise ~django.core.exceptions.FieldDoesNotExist: If a relation is
        pointing to the fields that don't exist.

    .. warning::
       The relations of an instance, a queryset or a list of instances
       **must** be fetched before performing the translation process.

       To do this use :meth:`~django.db.models.query.QuerySet.select_related`,
       :meth:`~django.db.models.query.QuerySet.prefetch_related` or
       :func:`~django.db.models.prefetch_related_objects`.

    .. warning::
       Only when all the filterings are executed on the relations of an
       instance, a queryset or a list of instances, they should go through the
       translation process, otherwise if a relation is filtered after the
       translation process the translations of that relation are reset.

       To filter a relation when fetching it use
       :class:`~django.db.models.Prefetch`.

    .. testsetup:: apply_translations

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

    To apply the translations on a list of instances and the relations of it:

    .. testcode:: apply_translations

       from django.db.models import prefetch_related_objects
       from sample.models import Continent, Country, City
       from translations.utils import apply_translations

       relations = ('countries', 'countries__cities',)

       continents = list(Continent.objects.all())
       prefetch_related_objects(continents, *relations)

       apply_translations(continents, *relations, lang="de")

       for continent in continents:
           print("Continent: {}".format(continent))
           for country in continent.countries.all():
               print("Country: {}".format(country))
               for city in country.cities.all():
                   print("City: {}".format(city))

    .. testoutput:: apply_translations

       Continent: Europa
       Country: Deutschland
       City: Köln
       City: München
       Continent: Asien
       Country: Südkorea
       City: Seül
       City: Ulsän

    To apply the translations on a queryset and the relations of it:

    .. testcode:: apply_translations

       from sample.models import Continent, Country, City
       from translations.utils import apply_translations

       relations = ('countries', 'countries__cities',)

       continents = Continent.objects.prefetch_related(*relations).all()

       apply_translations(continents, *relations, lang="de")

       for continent in continents:
           print("Continent: {}".format(continent))
           for country in continent.countries.all():
               print("Country: {}".format(country))
               for city in country.cities.all():
                   print("City: {}".format(city))

    .. testoutput:: apply_translations

       Continent: Europa
       Country: Deutschland
       City: Köln
       City: München
       Continent: Asien
       Country: Südkorea
       City: Seül
       City: Ulsän

    To apply the translations on an instance and the relations of it:

    .. testcode:: apply_translations

       from django.db.models import prefetch_related_objects
       from sample.models import Continent, Country, City
       from translations.utils import apply_translations

       relations = ('countries', 'countries__cities',)

       europe = Continent.objects.get(code="EU")
       prefetch_related_objects([europe], *relations)

       apply_translations(europe, *relations, lang="de")

       print("Continent: {}".format(europe))
       for country in europe.countries.all():
           print("Country: {}".format(country))
           for city in country.cities.all():
               print("City: {}".format(city))

    .. testoutput:: apply_translations

       Continent: Europa
       Country: Deutschland
       City: Köln
       City: München
    """
    hierarchy = _get_relations_hierarchy(*relations)

    dictionary = _get_translations_dictionary(
        _get_translations(
            entity,
            *relations,
            lang=lang
        )
    )

    _apply_entity_translations(entity, hierarchy, dictionary, included=True)


def update_translations(entity, lang=None):
    lang = _get_translation_language(lang)
    iterable, model = _get_entity_details(entity)

    # ------------ renew transaction
    if issubclass(model, translations.models.Translatable):
        translatable_fields = model.get_translatable_fields()
        try:
            with transaction.atomic():
                # ------------ delete old translations
                translations_queryset = _get_translations(
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
