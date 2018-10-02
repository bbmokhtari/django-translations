"""
This module contains the utilities for the Translations app. It contains the
following members:

:func:`_get_standard_language`
    Return the standard language code of a custom language code.
:func:`_get_entity_details`
    Return the iteration and type details of an entity.
:func:`_get_reverse_relation`
    Return the reverse of a model's relation.
:func:`_get_relations_hierarchy`
    Return the :term:`relations hierarchy` of some relations.
:func:`_get_instance_groups`
    Return the :term:`instance groups` of an entity and
    a :term:`relations hierarchy` of it.
:func:`_get_translations`
    Return the translations of some :term:`instance groups` in a language.
:class:`TranslationContext`
    A context manager which provides custom translation functionalities.
"""

from django.db import models
from django.db.models.query import prefetch_related_objects
from django.db.models.constants import LOOKUP_SEP
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import get_language
from django.conf import settings

from translations.models import Translation, Translatable


__docformat__ = 'restructuredtext'


def _get_standard_language(lang=None):
    """
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
    """
    lang = lang if lang else get_language()
    code = lang.split('-')[0]

    lang_exists = False
    code_exists = False

    # break when the lang is found but not when the code is found
    # cause the code might come before lang and we may miss an accent
    for language in settings.LANGUAGES:
        if lang == language[0]:
            lang_exists = True
            break
        if code == language[0]:
            code_exists = True

    if lang_exists:
        return lang
    elif code_exists:
        return code
    else:
        raise ValueError(
            'The language code `{}` is not supported.'.format(lang)
        )


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
    """
    error_message = '`{}` is neither {} nor {}.'.format(
        entity,
        'a model instance',
        'an iterable of model instances',
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

       # usage
       reverse_relation = _get_reverse_relation(Continent, 'countries__cities')

       # output
       print('City can be queried with `{}`'.format(reverse_relation))

    .. testoutput:: _get_reverse_relation

       City can be queried with `country__continent`
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
            reverse_relation,
        )
    else:
        return reverse_relation


def _get_relations_hierarchy(*relations):
    """
    Return the :term:`relations hierarchy` of some relations.

    Creates the :term:`relations hierarchy`, splits each relation into
    different parts based on the relation depth and fills the
    :term:`relations hierarchy` with them. When all the relations are
    processed returns the :term:`relations hierarchy`.

    :param relations: The relations to derive the :term:`relations hierarchy`
        out of.
        Each relation may be composed of many ``related_query_name``\\ s
        separated by :data:`~django.db.models.constants.LOOKUP_SEP`
        (usually ``__``) to represent a deeply nested relation.
    :type relations: list(str)
    :return: The :term:`relations hierarchy` derived out of the relations.
    :rtype: dict(str, dict)

    To get the :term:`relations hierarchy` of a first-level relation:

    .. testcode::

       from translations.utils import _get_relations_hierarchy

       # usage
       hierarchy = _get_relations_hierarchy('countries')

       # output
       print(hierarchy)

    .. testoutput::

       {'countries': {'included': True, 'relations': {}}}

    To get the :term:`relations hierarchy` of a second-level relation,
    not including the first-level relation:

    .. testcode::

       from translations.utils import _get_relations_hierarchy

       # usage
       hierarchy = _get_relations_hierarchy('countries__cities')

       # output
       print(hierarchy)

    .. testoutput::

       {'countries': {'included': False,
                      'relations': {'cities': {'included': True,
                                               'relations': {}}}}}

    To get the :term:`relations hierarchy` of a second-level relation,
    including the first-level relation:

    .. testcode::

       from translations.utils import _get_relations_hierarchy

       # usage
       hierarchy = _get_relations_hierarchy('countries', 'countries__cities')

       # output
       print(hierarchy)

    .. testoutput::

       {'countries': {'included': True,
                      'relations': {'cities': {'included': True,
                                               'relations': {}}}}}

    To get the :term:`relations hierarchy` of no relations:

    .. testcode::

       from translations.utils import _get_relations_hierarchy

       # usage
       hierarchy = _get_relations_hierarchy()

       # output
       print(hierarchy)

    .. testoutput::

       {}
    """
    hierarchy = {}

    def _fill_hierarchy(hierarchy, *relation_parts):
        root = relation_parts[0]
        nest = relation_parts[1:]

        hierarchy.setdefault(root, {
            'included': False,
            'relations': {},
        })

        if nest:
            _fill_hierarchy(hierarchy[root]['relations'], *nest)
        else:
            hierarchy[root]['included'] = True

    for relation in relations:
        parts = relation.split(LOOKUP_SEP)
        _fill_hierarchy(hierarchy, *parts)
    return hierarchy


def _get_instance_groups(entity, hierarchy):
    """
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
    """
    groups = {}

    def _fill_entity(entity, hierarchy, included=True):
        iterable, model = _get_entity_details(entity)

        if model is None:
            return

        content_type = ContentType.objects.get_for_model(model)

        if included:
            object_groups = groups.setdefault(content_type.id, {})
            if not issubclass(model, Translatable):
                raise TypeError('`{}` is not Translatable!'.format(model))

        def _fill_obj(obj):
            if included:
                obj._default_translatable_fields = {
                    field: getattr(obj, field) for field in
                    type(obj)._get_translatable_fields_names()
                }
                object_groups[str(obj.id)] = obj

            if hierarchy:
                for (relation, detail) in hierarchy.items():
                    try:
                        value = getattr(obj, relation)
                    except AttributeError:
                        # raise when no such rel
                        model._meta.get_field(relation)
                        value = None

                    if value is not None:
                        if isinstance(value, models.Manager):
                            if not (
                                hasattr(obj, '_prefetched_objects_cache') and
                                relation in obj._prefetched_objects_cache
                            ):
                                prefetch_related_objects([obj], relation)
                            value = value.all()
                        _fill_entity(
                            entity=value,
                            hierarchy=detail['relations'],
                            included=detail['included'],
                        )

        if iterable:
            for obj in entity:
                _fill_obj(obj)
        else:
            _fill_obj(entity)

    _fill_entity(entity, hierarchy)

    return groups


def _get_translations(groups, lang):
    """
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
    """
    filters = models.Q()
    for (ct_id, objs) in groups.items():
        for obj_id in objs:
            filters |= models.Q(
                content_type__id=ct_id,
                object_id=obj_id,
            )

    queryset = Translation.objects.filter(
        language=lang,
    ).filter(
        filters,
    ).select_related('content_type')

    return queryset


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
           from translations.utils import TranslationContext

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
           from translations.utils import TranslationContext

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
           from translations.utils import TranslationContext

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
           from translations.utils import TranslationContext

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
           from translations.utils import TranslationContext

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
           from translations.utils import TranslationContext

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
           from translations.utils import TranslationContext

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
           from translations.utils import TranslationContext

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
           from translations.utils import TranslationContext

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
              from translations.utils import TranslationContext

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
              from translations.utils import TranslationContext

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
           from translations.utils import TranslationContext

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
           from translations.utils import TranslationContext

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
           from translations.utils import TranslationContext

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
           from translations.utils import TranslationContext

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
           from translations.utils import TranslationContext

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
           from translations.utils import TranslationContext

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
