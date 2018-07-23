"""
This module contains the utilities for the Translations app.

.. rubric:: Functions:

:func:`get_validated_language`
    Return the validated given language code or the current active language
    code.
:func:`get_validated_context_info`
    Return the model and iteration information about the validated context.
:func:`get_reverse_relation`
    Return the reverse of a relation for a model.
:func:`get_translations_reverse_relation`
    Return the reverse of the translations relation for a model, or
    translations relation *of a relation* for the model.
:func:`get_translations`
    Return the translations of a context and the relations of it in a
    language.
:func:`get_dictionary`
    Return a dictionary which contains the translations.
"""

from django.db import models, transaction
from django.db.models.constants import LOOKUP_SEP
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import get_language
from django.conf import settings

import translations.models


__docformat__ = 'restructuredtext'


def get_validated_language(lang=None):
    """
    Return the validated given language code or the current active language
    code.

    :param lang: The language code to validate, ``None`` means the current
        active language
    :type lang: str or None
    :return: The validated language code
    :rtype: str
    :raise ValueError: If the language code is not included in
        the :data:`~django.conf.settings.LANGUAGES` settings

    >>> from django.utils.translation import activate
    >>> from translations.utils import get_validated_language
    >>> # An already active language
    >>> activate('en')
    >>> get_validated_language()
    'en'
    >>> # A custom language
    >>> get_validated_language('de')
    'de'
    >>> # A language that doesn't exist in `LANGUAGES`
    >>> get_validated_language('xx')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: The language code `xx` is not supported.
    """
    lang = lang if lang else get_language()

    if lang not in [language[0] for language in settings.LANGUAGES]:
        raise ValueError(
            "The language code `{}` is not supported.".format(lang)
        )

    return lang


def get_validated_context_info(context):
    """
    Return the model and iteration information about the validated context.

    :param context: The context to validate
    :type context: ~django.db.models.Model or
        ~collections.Iterable(~django.db.models.Model)
    :return: A tuple representing the context information as (model, iterable)
    :rtype: tuple(type(~django.db.models.Model), bool)
    :raise TypeError: If the context is neither a model instance nor
        an iterable of model instances

    >>> from places.models import Continent
    >>> from translations.utils import get_validated_context_info
    >>> # A model instance
    >>> europe = Continent.objects.create(code="EU", name="Europe")
    >>> get_validated_context_info(europe)
    (<class 'places.models.Continent'>, False)
    >>> # A model iterable
    >>> continents = Continent.objects.all()
    >>> get_validated_context_info(continents)
    (<class 'places.models.Continent'>, True)
    >>> # An empty queryset
    >>> continents.delete()
    (1, {'translations.Translation': 0, 'places.Continent': 1})
    >>> get_validated_context_info(continents)
    (None, True)
    >>> # An empty list
    >>> get_validated_context_info([])
    (None, True)
    >>> # An invalid type
    >>> get_validated_context_info(123)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: `123` is neither a model instance nor an iterable of model instances.
    """
    error_message = '`{}` is neither {} nor {}.'.format(
        context,
        'a model instance',
        'an iterable of model instances'
    )

    if isinstance(context, models.Model):
        model = type(context)
        iterable = False
    elif hasattr(context, '__iter__'):
        if len(context) > 0:
            if isinstance(context[0], models.Model):
                model = type(context[0])
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

    :param model: The model which contains the relation and which the reverse
        relation will point to
    :type model: type(~django.db.models.Model)
    :param relation: The relation of the model to get the reverse of -
        can include
        :data:`~django.db.models.constants.LOOKUP_SEP` (usually ``__``) to
        represent a deeply nested relation
    :type relation: str
    :return: The reverse of the relation
    :rtype: str
    :raise ~django.core.exceptions.FieldDoesNotExist: If the relation is
        pointing to the fields that don't exist

    >>> # Let's suppose we want a list of all the cities in Europe
    >>> from places.models import Continent, Country, City
    >>> from translations.utils import get_reverse_relation
    >>> europe = Continent.objects.create(code="EU", name="Europe")
    >>> germany = Country.objects.create(
    ...     code="DE",
    ...     name="Germany",
    ...     continent=europe
    ... )
    >>> cologne = City.objects.create(name="Cologne", country=germany)
    >>> # To get the cities:
    >>> get_reverse_relation(Continent, 'countries__cities')
    'country__continent'
    >>> # Using this reverse relation we can query `City` with a `Continent`
    >>> City.objects.filter(country__continent=europe)
    <TranslatableQuerySet [<City: Cologne>]>
    >>> # Done! Cities fetched.
    >>> # An invalid relation of the model
    >>> get_reverse_relation(Continent, 'countries__wrong')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    django.core.exceptions.FieldDoesNotExist: Country has no field named 'wrong'
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
    Return the reverse of the translations relation for a model, or
    translations relation *of a relation* for the model.

    :param model: The model which contains the translations relation directly
        or indirectly (meaning it contains the translations relation itself,
        or the specified relation has it) and which the reverse relation will
        point to
    :type model: type(~django.db.models.Model)
    :param relation: The relation of the model which contains the translations
        relation, to get the reverse of - can include
        :data:`~django.db.models.constants.LOOKUP_SEP` (usually ``__``) to
        represent a deeply nested relation, ``None`` means the translations
        relation is not for a relation but for the model itself
    :type relation: str or None
    :return: The reverse of the translations relation
    :rtype: str
    :raise ~django.core.exceptions.FieldDoesNotExist: If the relation is
        pointing to the fields that don't exist

    >>> # Let's suppose we want a list of all the cities translations
    >>> from places.models import Continent, Country, City
    >>> from translations.models import Translation
    >>> from translations.utils import get_translations_reverse_relation
    >>> europe = Continent.objects.create(code="EU", name="Europe")
    >>> germany = Country.objects.create(
    ...     code="DE",
    ...     name="Germany",
    ...     continent=europe
    ... )
    >>> cologne = City.objects.create(name="Cologne", country=germany)
    >>> cologne.translations.create(field="name", language="de", text="Köln")
    <Translation: Cologne: Köln>
    >>> # To get the city translations:
    >>> get_translations_reverse_relation(Continent, 'countries__cities')
    'places_city__country__continent'
    >>> # Using this translations reverse relation we can query the
    >>> # `Translation` for the `City` with a `Continent`
    >>> Translation.objects.filter(places_city__country__continent=europe)
    <QuerySet [<Translation: Cologne: Köln>]>
    >>> # Done! Cities translations fetched.
    >>> # Translations reverse relation of a model
    >>> get_translations_reverse_relation(Continent)
    'places_continent'
    >>> # An invalid relation of the model
    >>> get_translations_reverse_relation(Continent, 'countries__wrong')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    django.core.exceptions.FieldDoesNotExist: Country has no field named 'wrong'
    """
    if relation is None:
        translations_relation = 'translations'
    else:
        translations_relation = '{}__{}'.format(relation, 'translations')

    return get_reverse_relation(model, translations_relation)


def get_translations(context, *relations, lang=None):
    """
    Return the translations of a context and the relations of it in a
    language.

    This function collects all the reverse relations of the context and its
    relations to :class:`~translations.models.Translation` and uses them to
    query the database with the minimum amount of queries needed (usually
    one).

    :param context: The context to fetch the translations for
    :type context: ~django.db.models.Model or
        ~collections.Iterable(~django.db.models.Model)
    :param relations: The relations of the context to fetch the
        translations for
    :type relations: list(str)
    :param lang: The language to fetch the translations for, ``None`` means
        the current active language
    :type lang: str or None
    :return: The translations
    :rtype: ~django.db.models.query.QuerySet
    :raise ValueError: If the language code is not included in
        the :data:`~django.conf.settings.LANGUAGES` settings
    :raise TypeError: If the context is neither a model instance nor
        an iterable of model instances
    :raise ~django.core.exceptions.FieldDoesNotExist: If the relation is
        pointing to the fields that don't exist

    >>> # Let's suppose we want the translations of a continent and
    >>> # its countries and cities
    >>> from places.models import Continent, Country, City
    >>> from translations.utils import get_translations
    >>> europe = Continent.objects.create(code="EU", name="Europe")
    >>> europe.translations.create(field="name", language="de", text="Europa")
    <Translation: Europe: Europa>
    >>> germany = Country.objects.create(
    ...     code="DE",
    ...     name="Germany",
    ...     continent=europe
    ... )
    >>> germany.translations.create(
    ...     field="name",
    ...     language="de",
    ...     text="Deutschland"
    ... )
    <Translation: Germany: Deutschland>
    >>> cologne = City.objects.create(name="Cologne", country=germany)
    >>> cologne.translations.create(field="name", language="de", text="Köln")
    <Translation: Cologne: Köln>
    >>> # To get the translations:
    >>> get_translations(europe, "countries", "countries__cities", lang="de")
    <QuerySet [<Translation: Europe: Europa>, <Translation: Germany: Deutschland>, <Translation: Cologne: Köln>]>
    >>> # Done! translations fetched.
    >>> # An invalid relation of the model
    >>> get_translations(europe, "countries", "countries__cities", lang="xx")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: The language code `xx` is not supported.
    >>> get_translations(123, "countries", "countries__cities", lang="de")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: `123` is neither a model instance nor an iterable of model instances.
    >>> get_translations(europe, "countries", "countries__wrong", lang="de")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    django.core.exceptions.FieldDoesNotExist: Country has no field named 'wrong'
    """
    lang = get_validated_language(lang)
    model, iterable = get_validated_context_info(context)

    if model is None:
        return translations.models.Translation.objects.none()

    if iterable:
        condition = 'pk__in'
        value = [instance.pk for instance in context]
    else:
        condition = 'pk'
        value = context.pk

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


def get_dictionary(translations):
    """
    Return a dictionary which contains the translations.

    The end result is something like this:
    ``{content_type_id: {object_id: {field1: text1, field2: text2}}}``

    :param translations: the translations to process
    :type translations: ~django.db.models.query.QuerySet
    :return: the dictionary of translations
    :rtype: dict(int, dict(str, dict(str, str)))

    >>> from places.models import Continent, Country, City
    >>> from translations.models import Translation
    >>> europe = Continent.objects.create(code="EU", name="Europe")
    >>> europe.translations.create(field="name", language="de", text="Europa")
    <Translation: Europe: Europa>
    >>> germany = Country.objects.create(
    ...     code="DE",
    ...     name="Germany",
    ...     continent=europe
    ... )
    >>> germany.translations.create(
    ...     field="name",
    ...     language="de",
    ...     text="Deutschland"
    ... )
    <Translation: Germany: Deutschland>
    >>> cologne = City.objects.create(name="Cologne", country=germany)
    >>> cologne.translations.create(field="name", language="de", text="Köln")
    <Translation: Cologne: Köln>
    >>> get_dictionary(Translation.objects.all())
    {2: {'1': {'name': 'Europa'}},
    3: {'1': {'name': 'Deutschland'}},
    1: {'1': {'name': 'Köln'}}}
    """
    dictionary = {}

    for translation in translations:
        content_type_id = translation.content_type.id
        object_id = translation.object_id
        field = translation.field

        if content_type_id not in dictionary.keys():
            dictionary[content_type_id] = {}

        if object_id not in dictionary[content_type_id].keys():
            dictionary[content_type_id][object_id] = {}

        dictionary[content_type_id][object_id][field] = translation.text

    return dictionary


def get_hierarchy(*relations):
    """
    Return a hierarchy of the relations.

    >>> get_hierarchy()
    {}
    >>> get_hierarchy('countries')
    {'countries': {'included': True, 'relations': []}}
    >>> get_hierarchy('countries__cities')
    {'countries': {'included': False, 'relations': ['cities']}}
    >>> get_hierarchy('countries', 'countries__cities')
    {'countries': {'included': True, 'relations': ['cities']}}

    :param relations: a list of relations.
    :type relations: list(str)
    :return: the relations hierarchy
    :rtype: dict(str, list(str))
    """
    hierarchy = {}

    for relation in relations:
        parts = relation.split(LOOKUP_SEP)

        root = parts[0]
        nest = LOOKUP_SEP.join(parts[1:])

        if root not in hierarchy.keys():
            hierarchy[root] = {
                "included": False,
                "relations": []
            }

        if nest:
            hierarchy[root]["relations"].append(nest)
        else:
            hierarchy[root]["included"] = True

    return hierarchy


def translate(context, *relations, lang=None, dictionary=None, included=True):
    lang = get_validated_language(lang)
    model, iterable = get_validated_context_info(context)

    if model is None:
        return

    if dictionary is None:
        dictionary = get_dictionary(
            get_translations(
                context,
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
                for obj in context:
                    translate_obj(obj)
            else:
                translate_obj(context)

    hierarchy = get_hierarchy(*relations)
    if hierarchy:
        def translate_rel(obj):
            for (relation, details) in hierarchy.items():
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
            for obj in context:
                translate_rel(obj)
        else:
            translate_rel(context)


def update_translations(context, lang=None):
    lang = get_validated_language(lang)
    model, iterable = get_validated_context_info(context)

    # ------------ renew transaction
    if issubclass(model, translations.models.Translatable):
        translatable_fields = model.get_translatable_fields()
        try:
            with transaction.atomic():
                # ------------ delete old translations
                translations_queryset = get_translations(
                    context,
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
                    for obj in context:
                        add_translations(obj)
                else:
                    add_translations(context)

                if len(translations_objects) > 0:
                    translations.models.Translation.objects.bulk_create(translations_objects)
        except Exception:
            raise
