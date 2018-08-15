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
:func:`get_relations_details`
    Return the details of the relations.
:func:`translate`
    Translate the entity.
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
           for city in country.cities.all():
               print("City: {}".format(city.name))

    .. testoutput:: get_reverse_relation

       City: Cologne
       City: Munich

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
       for city in cities:
           print("City: {}".format(city.name))

    .. testoutput:: get_reverse_relation

       City can be queried with 'country__continent'
       City: Cologne
       City: Munich

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
           continent_fields=["name"],
           country_fields=["name"],
           city_fields=["name"],
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
               for translation in city.translations.all():
                   print("City: {}".format(translation.text))

    .. testoutput:: get_translations_reverse_relation

       City: Köln
       City: München

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
       for translation in translations:
           print("City: {}".format(translation.text))

    .. testoutput:: get_translations_reverse_relation

       Translation can be queried with 'sample_city__country__continent'
       City: Köln
       City: München

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
       for translation in translations:
           print("Continent: {}".format(translation.text))

    .. testoutput:: get_translations_reverse_relation

       Translation can be queried with 'sample_continent'
       Continent: Europa
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
           city_names=["cologne", "seoul"],
           continent_fields=["name"],
           country_fields=["name"],
           city_fields=["name"],
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

       # print translations
       print(translations)

    .. testoutput:: get_translations

       <QuerySet [<Translation: Europe: Europa>, <Translation: Germany: ...

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

       # print translations
       print(translations)

    .. testoutput:: get_translations

       <QuerySet [<Translation: Europe: Europa>, <Translation: Germany: ...

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

       # print translations
       print(translations)

    .. testoutput:: get_translations

       <QuerySet [<Translation: Europe: Europa>, <Translation: Germany: ...

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

    .. note::
       Always filter the ``translations`` in a language before passing it in,
       otherwise the other language may override some fields of the initial
       language and a translations dictionary with mixed content gets
       outputted which is not what's desired.

    .. testsetup:: get_translations_dictionary

       from tests.sample import create_samples

       create_samples(
           continent_names=["europe", "asia"],
           country_names=["germany", "south korea"],
           city_names=["cologne", "seoul"],
           continent_fields=["name", "denonym"],
           country_fields=["name", "denonym"],
           city_fields=["name", "denonym"],
           langs=["de"]
       )

    To get the translations dictionary of all the translations.

    .. testcode:: get_translations_dictionary

       from translations.utils import get_translations_dictionary
       from translations.models import Translation

       translations = Translation.objects.filter(language="de")
       print(get_translations_dictionary(translations))

    .. testoutput:: get_translations_dictionary

       {8: {'1': {'denonym': 'Kölner', 'name': 'Köln'},
            '2': {'denonym': 'Seülisch', 'name': 'Seül'}},
        9: {'1': {'denonym': 'Europäisch', 'name': 'Europa'},
            '2': {'denonym': 'Asiatisch', 'name': 'Asien'}},
        10: {'1': {'denonym': 'Deutsche', 'name': 'Deutschland'},
             '2': {'denonym': 'Südkoreanisch', 'name': 'Südkorea'}}}

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


def get_relations_details(*relations):
    """
    Return the details of the relations.

    :param relations: The relations to get the details of
    :type relations: list(str)
    :return: The relations details
    :rtype: dict(str, dict)

    """
    # >>> get_relations_details()
    # {}
    # >>> get_relations_details('countries')
    # {'countries': {'included': True, 'relations': []}}
    # >>> get_relations_details('countries__cities')
    # {'countries': {'included': False, 'relations': ['cities']}}
    # >>> get_relations_details('countries', 'countries__cities')
    # {'countries': {'included': True, 'relations': ['cities']}}
    details = {}

    for relation in relations:
        parts = relation.split(LOOKUP_SEP)

        root = parts[0]
        nest = LOOKUP_SEP.join(parts[1:])

        details.setdefault(root, {
            "included": False,
            "relations": []
        })

        if nest:
            details[root]["relations"].append(nest)
        else:
            details[root]["included"] = True

    return details


def translate(entity, *relations, lang=None, dictionary=None, included=True):
    """
    Translate the entity.

    This function translates the entity and its relations using a dictionary.
    If the dictionary isn't provided it will fetch all the translations for
    the entity and its relations in a language using :func:`get_translations`
    and convert them to a dictionary using :func:`get_translations_dictionary` and use that
    for translation.

    :param entity: The entity to translate
    :type entity: ~django.db.models.Model or
        ~collections.Iterable(~django.db.models.Model)
    :param relations: The relations of the entity to translate
    :type relations: list(str)
    :param lang: The language to translate the entity and its relations in,
        ``None`` means the current active language
    :type lang: str or None
    :param dictionary: The dictionary to use for translation, ``None`` means
        create the dictionary automatically
    :type dictionary: dict(int, dict(str, dict(str, str))) or None
    :param included: Whether the entity should be translated itself along
        with the relations or not, the default is ``True``
    :type included: bool
    :raise ValueError: If the language code is not included in
        the :data:`~django.conf.settings.LANGUAGES` settings
    :raise TypeError: If the entity is neither a model instance nor
        an iterable of model instances
    :raise ~django.core.exceptions.FieldDoesNotExist: If the relation is
        pointing to the fields that don't exist

    .. note::
       Always use :meth:`~django.db.models.query.QuerySet.select_related`,
       :meth:`~django.db.models.query.QuerySet.prefetch_related` or
       :func:`~django.db.models.prefetch_related_objects` for fetching the
       relations of the entity before using :func:`translate`.

    """
    # .. testsetup:: translate

    #    from sample.models import Continent, Country, City
    #    from translations.utils import translate
    #    europe = Continent.objects.create(
    #        code="EU",
    #        name="Europe",
    #        denonym="European",
    #    )
    #    europe.translations.create(
    #        field="name",
    #        language="de",
    #        text="Europa"
    #    )
    #    europe.translations.create(
    #        field="denonym",
    #        language="de",
    #        text="Europäisch"
    #    )
    #    germany = Country.objects.create(
    #        code="DE",
    #        name="Germany",
    #        denonym="German",
    #        continent=europe
    #    )
    #    germany.translations.create(
    #        field="name",
    #        language="de",
    #        text="Deutschland"
    #    )
    #    germany.translations.create(
    #        field="denonym",
    #        language="de",
    #        text="Deutsche"
    #    )
    #    cologne = City.objects.create(
    #        name="Cologne",
    #        denonym="Cologner",
    #        country=germany
    #    )
    #    cologne.translations.create(
    #        field="name",
    #        language="de",
    #        text="Köln"
    #    )
    #    cologne.translations.create(
    #        field="denonym",
    #        language="de",
    #        text="Kölner"
    #    )

    # .. doctest:: translate

    #    >>> # MAKE SURE: `select_related` and `prefetch_related`
    #    >>> europe = Continent.objects.prefetch_related(
    #    ...     'countries',
    #    ...     'countries__cities',
    #    ... ).get(code="EU")
    #    >>> # Translate:
    #    >>> translate(europe, "countries", "countries__cities", lang="de")
    #    >>> # Done!
    #    >>> germany = europe.countries.all()[0]
    #    >>> cologne = germany.cities.all()[0]
    #    >>> europe.name
    #    Europa
    #    >>> europe.denonym
    #    Europäisch
    #    >>> germany.name
    #    Deutschland
    #    >>> germany.denonym
    #    Deutsche
    #    >>> cologne.name
    #    Köln
    #    >>> cologne.denonym
    #    Kölner
    lang = get_translation_language(lang)
    model, iterable = get_entity_details(entity)

    if model is None:
        return

    if dictionary is None:
        dictionary = get_translations_dictionary(
            get_translations(
                entity,
                *relations,
                lang=lang
            )
        )

    if included:
        content_type = ContentType.objects.get_for_model(model)
        objects = dictionary[content_type.id]
        if objects:
            def translate_obj(obj):
                try:
                    fields = objects[str(obj.id)]
                except KeyError:
                    pass
                else:
                    for (field, text) in fields.items():
                        setattr(obj, field, text)

            if iterable:
                for obj in entity:
                    translate_obj(obj)
            else:
                translate_obj(entity)

    details = get_relations_details(*relations)
    if details:
        def translate_rel(obj):
            for (relation, details) in details.items():
                value = getattr(obj, relation, None)
                if value is not None:
                    if isinstance(value, models.Manager):
                        value = value.all()
                    translate(
                        value,
                        *details['relations'],
                        lang=lang,
                        dictionary=dictionary,
                        included=details['included'],
                    )

        if iterable:
            for obj in entity:
                translate_rel(obj)
        else:
            translate_rel(entity)


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
