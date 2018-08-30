"""
This module contains the utilities for the Translations app.

.. rubric:: Functions:

:func:`_get_translation_language`
    Return a language code to use in the translation process.
:func:`_get_entity_details`
    Return the iteration and type details of an entity.
:func:`_get_reverse_relation`
    Return the reverse of a model's relation.
:func:`_get_relations_hierarchy`
    Return the :term:`relations hierarchy` made out of some relations.
:func:`_get_entity_groups`
    Return the :term:`entity groups` made out of an entity and
    a :term:`relations hierarchy` of it.
:func:`_get_translations`
    Return the translations of some :term:`entity groups` in a language.
:func:`apply_translations`
    Apply the translations on an entity and the relations of it in a language.
:func:`update_translations`
    Update the translations of an entity and the relations of it in a
    language.
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
       even if the iterable is an empty queryset (which the model of can be
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
    back to the model.

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


def _get_relations_hierarchy(*relations):
    """
    Return the :term:`relations hierarchy` made out of some relations.

    Processes the relations and returns the :term:`relations hierarchy` made
    out of them.

    :param relations: The relations to make the :term:`relations hierarchy`
        out of.
    :type relations: list(str)
    :return: The :term:`relations hierarchy` made out of the relations.
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

    def _fill_hierarchy(hierarchy, *relation_parts):
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

    for relation in relations:
        parts = relation.split(LOOKUP_SEP)
        _fill_hierarchy(hierarchy, *parts)
    return hierarchy


def _get_entity_groups(entity, hierarchy):
    """
    Return the :term:`entity groups` made out of an entity and
    a :term:`relations hierarchy` of it.

    Processes the entity and the :term:`relations hierarchy` of it and returns
    the :term:`entity groups` made out of them.

    :param entity: the entity to make the :term:`entity groups` out of and out
        of the :term:`relations hierarchy` of.
    :type entity: ~django.db.models.Model or
        ~collections.Iterable(~django.db.models.Model)
    :param hierarchy: The :term:`relations hierarchy` of the entity to make
        the :term:`entity groups` out of.
    :type hierarchy: dict(str, dict)
    :return: The :term:`entity groups` made out of the entity and
        the :term:`relations hierarchy` of it.
    :rtype: dict(int, dict(str, ~django.db.models.Model))
    :raise TypeError:

        - If the entity is neither a model instance nor
          an iterable of model instances.

        - If the model of the entity or the model of the included relations is
          not :class:`~translations.models.Translatable`.

    :raise ~django.core.exceptions.FieldDoesNotExist: If a relation is
        pointing to the fields that don't exist.

    .. testsetup:: _get_entity_groups

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

    To get the :term:`entity groups` of an entity and
    the :term:`relations hierarchy` of it:

    .. testcode:: _get_entity_groups

       from django.contrib.contenttypes.models import ContentType
       from sample.models import Continent, Country, City
       from translations.utils import _get_entity_groups
       from translations.utils import _get_relations_hierarchy

       relations = ('countries', 'countries__cities',)
       hierarchy = _get_relations_hierarchy(*relations)

       continents = Continent.objects.all()

       groups = _get_entity_groups(continents, hierarchy)

       ct_continent = ContentType.objects.get_for_model(Continent).id
       ct_country = ContentType.objects.get_for_model(Country).id
       ct_city = ContentType.objects.get_for_model(City).id

       for id, obj in sorted(groups[ct_continent].items(), key=lambda x: x[0]):
           print(obj)
       for id, obj in sorted(groups[ct_country].items(), key=lambda x: x[0]):
           print(obj)
       for id, obj in sorted(groups[ct_city].items(), key=lambda x: x[0]):
           print(obj)

    .. testoutput:: _get_entity_groups

       Europe
       Asia
       Germany
       South Korea
       Cologne
       Munich
       Seoul
       Ulsan
    """
    groups = {}

    def _fill_entity(entity, hierarchy, groups, included=True):
        iterable, model = _get_entity_details(entity)

        if model is None:
            return

        content_type = ContentType.objects.get_for_model(model)

        if included:
            content_type_groups = groups.setdefault(content_type.id, {})
            if not issubclass(model, translations.models.Translatable):
                raise TypeError('`{}` is not Translatable!'.format(model))

        def _fill_obj(obj, hierarchy):
            if included:
                content_type_groups[str(obj.id)] = obj

            if hierarchy:
                for (relation, detail) in hierarchy.items():
                    model._meta.get_field(relation)  # raise when no such rel
                    value = getattr(obj, relation, None)
                    if value is not None:
                        if isinstance(value, models.Manager):
                            value = value.all()
                        _fill_entity(
                            entity=value,
                            hierarchy=detail['relations'],
                            groups=groups,
                            included=detail['included']
                        )

        if iterable:
            for obj in entity:
                _fill_obj(obj, hierarchy)
        else:
            _fill_obj(entity, hierarchy)

    _fill_entity(entity, hierarchy, groups)

    return groups


def _get_translations(groups, lang=None):
    """
    Return the translations of some :term:`entity groups` in a language.

    Fetches the translations of the :term:`entity groups` in a language and
    returns them as a :class:`~translations.models.Translation` queryset.

    :param groups: The :term:`entity groups` to fetch the translations of.
    :type groups: dict(int, dict(str, ~django.db.models.Model))
    :param lang: The language to fetch the translations of
        the :term:`entity groups` in.
        ``None`` means use the :term:`active language` code.
    :type lang: str or None
    :return: The translations.
    :rtype: ~django.db.models.query.QuerySet(~translations.models.Translation)
    :raise ValueError: If the language code is not included in
        the :data:`~django.conf.settings.LANGUAGES` setting.

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

    To get the translations of some :term:`entity groups`:

    .. testcode:: _get_translations

       from sample.models import Continent
       from translations.utils import _get_relations_hierarchy
       from translations.utils import _get_entity_groups
       from translations.utils import _get_translations

       relations = ('countries','countries__cities',)

       continents = list(Continent.objects.all())
       hierarchy = _get_relations_hierarchy(*relations)
       groups = _get_entity_groups(continents, hierarchy)

       translations = _get_translations(groups, lang="de")

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
    """
    lang = _get_translation_language(lang)

    filters = models.Q()
    for (ct_id, objs) in groups.items():
        for obj_id in objs:
            filters |= models.Q(
                content_type__id=ct_id,
                object_id=obj_id
            )

    queryset = translations.models.Translation.objects.filter(
        language=lang
    ).filter(
        filters
    ).distinct().select_related('content_type')

    return queryset


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
    :raise TypeError:

        - If the entity is neither a model instance nor
          an iterable of model instances.

        - If the model of the entity or the model of the included relations is
          not :class:`~translations.models.Translatable`.

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
    groups = _get_entity_groups(entity, hierarchy)
    translations = _get_translations(groups, lang=lang)

    for translation in translations:
        ct_id = translation.content_type.id
        obj_id = translation.object_id
        obj = groups[ct_id][obj_id]

        field = translation.field
        text = translation.text

        if field in [x.name for x in type(obj).get_translatable_fields()]:
            setattr(obj, field, text)


def update_translations(entity, *relations, lang=None):
    """
    Update the translations of an entity and the relations of it in a
    language.

    Deletes the old translations of the entity and the specified relations of
    it in a language and creates new translations for them based on their
    fields values.

    :param entity: The entity to update the translations of and update the
        translations of the relations of.
    :type entity: ~django.db.models.Model or
        ~collections.Iterable(~django.db.models.Model)
    :param relations: The relations of the entity to update the translations
        of.
    :type relations: list(str)
    :param lang: The language to update the translations in.
        ``None`` means use the :term:`active language` code.
    :type lang: str or None
    :raise ValueError: If the language code is not included in
        the :data:`~django.conf.settings.LANGUAGES` setting.
    :raise TypeError:

        - If the entity is neither a model instance nor
          an iterable of model instances.

        - If the model of the entity or the model of the included relations is
          not :class:`~translations.models.Translatable`.

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

    .. testsetup:: update_translations

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

    To update the translations of a list of instances and the relations of it:

    .. testcode:: update_translations

       from django.db.models import prefetch_related_objects
       from sample.models import Continent, Country, City
       from translations.utils import update_translations

       relations = ('countries', 'countries__cities',)

       continents = list(Continent.objects.all())
       prefetch_related_objects(continents, *relations)

       update_translations(continents, *relations, lang="en")

       for continent in continents:
           print("Continent: {}".format(continent))
           for country in continent.countries.all():
               print("Country: {}".format(country))
               for city in country.cities.all():
                   print("City: {}".format(city))

    .. testoutput:: update_translations

       Continent: Europe
       Country: Germany
       City: Cologne
       City: Munich
       Continent: Asia
       Country: South Korea
       City: Seoul
       City: Ulsan

    To update the translations of a queryset and the relations of it:

    .. testcode:: update_translations

       from sample.models import Continent, Country, City
       from translations.utils import update_translations

       relations = ('countries', 'countries__cities',)

       continents = Continent.objects.prefetch_related(*relations).all()

       update_translations(continents, *relations, lang="en")

       for continent in continents:
           print("Continent: {}".format(continent))
           for country in continent.countries.all():
               print("Country: {}".format(country))
               for city in country.cities.all():
                   print("City: {}".format(city))

    .. testoutput:: update_translations

       Continent: Europe
       Country: Germany
       City: Cologne
       City: Munich
       Continent: Asia
       Country: South Korea
       City: Seoul
       City: Ulsan

    To update the translations of an instance and the relations of it:

    .. testcode:: update_translations

       from django.db.models import prefetch_related_objects
       from sample.models import Continent, Country, City
       from translations.utils import update_translations

       relations = ('countries', 'countries__cities',)

       europe = Continent.objects.get(code="EU")
       prefetch_related_objects([europe], *relations)

       update_translations(europe, *relations, lang="en")

       print("Continent: {}".format(europe))
       for country in europe.countries.all():
           print("Country: {}".format(country))
           for city in country.cities.all():
               print("City: {}".format(city))

    .. testoutput:: update_translations

       Continent: Europe
       Country: Germany
       City: Cologne
       City: Munich
    """
    lang = _get_translation_language(lang)

    hierarchy = _get_relations_hierarchy(*relations)
    groups = _get_entity_groups(entity, hierarchy)
    old_translations = _get_translations(groups, lang=lang)

    new_translations = []
    for (ct_id, objs) in groups.items():
        for (obj_id, obj) in objs.items():
            for field in type(obj).get_translatable_fields():
                text = getattr(obj, field.name, None)
                if text:
                    new_translations.append(
                        translations.models.Translation(
                            content_type_id=ct_id,
                            object_id=obj_id,
                            field=field.name,
                            language=lang,
                            text=text,
                        )
                    )

    old_translations.delete()
    translations.models.Translation.objects.bulk_create(new_translations)
