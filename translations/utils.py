"""
This module contains the utilities for the Translations app.

.. rubric:: Functions:

:func:`get_translation_language`
    Return the given language code or the current active language code.
:func:`get_context_details`
    Return the model and iteration details of the context.
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
:func:`get_relations_details`
    Return the details of the relations.
:func:`translate`
    Translate the context.
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
    Return the given language code or the current active language code.

    :param lang: The language code to validate, ``None`` means the current
        active language
    :type lang: str or None
    :return: The validated language code
    :rtype: str
    :raise ValueError: If the language code is not included in
        the :data:`~django.conf.settings.LANGUAGES` settings

    .. testsetup:: get_translation_language

       from django.utils.translation import activate

       activate('en')

    .. testcode:: get_translation_language

       from translations.utils import get_translation_language

       # Current active language in Django
       default = get_translation_language()
       print("default: {}".format(default))

       # Don't use the current active language
       custom = get_translation_language('de')
       print("custom: {}".format(custom))

    .. testoutput:: get_translation_language

       default: en
       custom: de
    """
    lang = lang if lang else get_language()

    if lang not in [language[0] for language in settings.LANGUAGES]:
        raise ValueError(
            "The language code `{}` is not supported.".format(lang)
        )

    return lang


def get_context_details(context):
    """
    Return the model and iteration details of the context.

    :param context: The context to validate
    :type context: ~django.db.models.Model or
        ~collections.Iterable(~django.db.models.Model)
    :return: A tuple representing the context information as (model, iterable)
    :rtype: tuple(type(~django.db.models.Model), bool)
    :raise TypeError: If the context is neither a model instance nor
        an iterable of model instances

    .. testsetup:: get_context_details

       from tests.sample import create_samples

       create_samples(continent_names=["europe"])

    .. testcode:: get_context_details

       from sample.models import Continent
       from translations.utils import get_context_details

       # Let's check a single object
       europe = Continent.objects.get(code="EU")
       details = get_context_details(europe)
       print("europe model is: {}".format(details[0]))
       print("is europe iterable? {}".format(details[1]))

       # Now an iterable object
       continents = Continent.objects.all()
       details = get_context_details(continents)
       print("continents model is: {}".format(details[0]))
       print("is continents iterable? {}".format(details[1]))

       # Now an empty iterable object
       empty = []
       details = get_context_details(empty)
       print("empty model is: {}".format(details[0]))
       print("is empty iterable? {}".format(details[1]))

    .. testoutput:: get_context_details

       europe model is: <class 'sample.models.Continent'>
       is europe iterable? False
       continents model is: <class 'sample.models.Continent'>
       is continents iterable? True
       empty model is: None
       is empty iterable? True
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

    .. testsetup::

       from tests.sample import create_samples

       create_samples(
           continent_names=["europe"],
           country_names=["germany", "turkey"],
           city_names=["cologne", "munich", "istanbul", "izmir"]
       )

    .. testcode::

       from sample.models import Continent, City
       from translations.utils import get_reverse_relation

       # Let's suppose we want a list of all the cities in Europe
       europe = Continent.objects.get(code="EU")
       reverse_field = get_reverse_relation(Continent, 'countries__cities')
       print("City can be queried with '{}'".format(reverse_field))
       cities = City.objects.filter(**{reverse_field: europe})
       print("cities in europe: {}".format([city.name for city in cities]))

    .. testoutput::

       City can be queried with 'country__continent'
       cities in europe: ['Cologne', 'Munich', 'Istanbul', 'Izmir']
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

    """
    # >>> # Let's suppose we want a list of all the cities translations
    # >>> from sample.models import Continent, Country, City
    # >>> from translations.models import Translation
    # >>> from translations.utils import get_translations_reverse_relation
    # >>> europe = Continent.objects.create(code="EU", name="Europe")
    # >>> germany = Country.objects.create(
    # ...     code="DE",
    # ...     name="Germany",
    # ...     continent=europe
    # ... )
    # >>> cologne = City.objects.create(name="Cologne", country=germany)
    # >>> cologne.translations.create(field="name", language="de", text="Köln")
    # <Translation: Cologne: Köln>
    # >>> # To get the city translations:
    # >>> get_translations_reverse_relation(Continent, 'countries__cities')
    # 'sample_city__country__continent'
    # >>> # Using this translations reverse relation we can query the
    # >>> # `Translation` for the `City` with a `Continent`
    # >>> Translation.objects.filter(sample_city__country__continent=europe)
    # <QuerySet [<Translation: Cologne: Köln>]>
    # >>> # Done! Cities translations fetched.
    # >>> # Translations reverse relation of a model
    # >>> get_translations_reverse_relation(Continent)
    # 'sample_continent'
    # >>> # An invalid relation of the model
    # >>> get_translations_reverse_relation(Continent, 'countries__wrong')
    # Traceback (most recent call last):
    #   File "<stdin>", line 1, in <module>
    # django.core.exceptions.FieldDoesNotExist: Country has no field named 'wrong'
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

    .. testsetup:: get_translations

       from tests.sample import create_samples

       create_samples(
           continent_names=["europe"],
           country_names=["germany"],
           city_names=["cologne"],
           continent_fields=["name", "denonym"],
           country_fields=["name", "denonym"],
           city_fields=["name", "denonym"],
           langs=["de"]
       )

    .. testcode:: get_translations

       from sample.models import Continent, Country, City
       from translations.utils import get_translations

       # objects: continent: europe, country: germany and city: cologne
       europe = Continent.objects.prefetch_related(
           'countries', 'countries__cities'
        ).get(name="Europe")

       # The translations for europe and all its relations in German
       translations = get_translations(
           europe,
           "countries", "countries__cities",
           lang="de"
       )

       # print translations
       for translation in translations:
           print(
               "{object}.{field} ({origin}) in '{lang}' is '{text}'".format(
                   object=translation.content_object,
                   field=translation.field,
                   origin=getattr(
                       translation.content_object,
                       translation.field
                   ),
                   lang=translation.language,
                   text=translation.text
               )
           )

    .. testoutput:: get_translations

       Europe.name (Europe) in 'de' is 'Europa'
       Europe.denonym (European) in 'de' is 'Europäisch'
       Germany.name (Germany) in 'de' is 'Deutschland'
       Germany.denonym (German) in 'de' is 'Deutsche'
       Cologne.name (Cologne) in 'de' is 'Köln'
       Cologne.denonym (Cologner) in 'de' is 'Kölner'
    """
    lang = get_translation_language(lang)
    model, iterable = get_context_details(context)

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

    The end result is something like this::

        {
            content_type_id_1: {
                object_id_1: {
                    field_1: text_1,
                    field_2: ...
                },
                object_id_2: ...
            },
            content_type_id_2: ...
        }

    The ``content_type_id`` represents the
    :class:`~django.contrib.contenttypes.models.ContentType` ID, ``object_id``
    represents the ID of the object in that content type, ``field``
    represents the name of the field for that object.

    :param translations: The translations to process
    :type translations: ~django.db.models.query.QuerySet
    :return: The dictionary of translations
    :rtype: dict(int, dict(str, dict(str, str)))

    """
    # >>> from sample.models import Continent, Country, City
    # >>> from translations.models import Translation
    # >>> europe = Continent.objects.create(
    # ...     code="EU",
    # ...     name="Europe"
    # ...     denonym="European",
    # ... )
    # >>> europe.translations.create(
    # ...     field="name",
    # ...     language="de",
    # ...     text="Europa"
    # ... )
    # <Translation: Europe: Europa>
    # >>> europe.translations.create(
    # ...     field="denonym",
    # ...     language="de",
    # ...     text="Europäisch"
    # ... )
    # <Translation: European: Europäisch>
    # >>> germany = Country.objects.create(
    # ...     code="DE",
    # ...     name="Germany",
    # ...     continent=europe
    # ... )
    # >>> germany.translations.create(
    # ...     field="name",
    # ...     language="de",
    # ...     text="Deutschland"
    # ... )
    # <Translation: Germany: Deutschland>
    # >>> cologne = City.objects.create(name="Cologne", country=germany)
    # >>> cologne.translations.create(field="name", language="de", text="Köln")
    # <Translation: Cologne: Köln>
    # >>> get_dictionary(Translation.objects.all())
    # {2: {'1': {'name': 'Europa', 'denonym': 'Europäisch'}},
    # 3: {'1': {'name': 'Deutschland'}},
    # 1: {'1': {'name': 'Köln'}}}
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


def translate(context, *relations, lang=None, dictionary=None, included=True):
    """
    Translate the context.

    This function translates the context and its relations using a dictionary.
    If the dictionary isn't provided it will fetch all the translations for
    the context and its relations in a language using :func:`get_translations`
    and convert them to a dictionary using :func:`get_dictionary` and use that
    for translation.

    :param context: The context to translate
    :type context: ~django.db.models.Model or
        ~collections.Iterable(~django.db.models.Model)
    :param relations: The relations of the context to translate
    :type relations: list(str)
    :param lang: The language to translate the context and its relations in,
        ``None`` means the current active language
    :type lang: str or None
    :param dictionary: The dictionary to use for translation, ``None`` means
        create the dictionary automatically
    :type dictionary: dict(int, dict(str, dict(str, str))) or None
    :param included: Whether the context should be translated itself along
        with the relations or not, the default is ``True``
    :type included: bool
    :raise ValueError: If the language code is not included in
        the :data:`~django.conf.settings.LANGUAGES` settings
    :raise TypeError: If the context is neither a model instance nor
        an iterable of model instances
    :raise ~django.core.exceptions.FieldDoesNotExist: If the relation is
        pointing to the fields that don't exist

    .. note::
       Always use :meth:`~django.db.models.query.QuerySet.select_related`,
       :meth:`~django.db.models.query.QuerySet.prefetch_related` or
       :func:`~django.db.models.prefetch_related_objects` for fetching the
       relations of the context before using :func:`translate`.

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
    model, iterable = get_context_details(context)

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
            for obj in context:
                translate_rel(obj)
        else:
            translate_rel(context)


def update_translations(context, lang=None):
    lang = get_translation_language(lang)
    model, iterable = get_context_details(context)

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
