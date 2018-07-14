"""
This module contains the utilities for the Translations app.

.. rubric:: Functions:

:func:`get_validated_language`
    Return the validated given language code or the current active language
    code.
"""

from django.db import models, transaction
from django.db.models.constants import LOOKUP_SEP
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import get_language

import translations.models
from translations.validators import validate_language


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
    :raise ~django.core.exceptions.ValidationError: If the language code is
        not supported in the :data:`~django.conf.settings.LANGUAGES` settings.

    >>> from django.utils.translation import activate
    >>> activate('en')
    >>> get_validated_language()
    'en'
    >>> get_validated_language('de')
    'de'
    >>> get_validated_language('xx')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    django.core.exceptions.ValidationError: ['The language code `xx` is not supported.']
    """
    lang = lang if lang else get_language()
    validate_language(lang)
    return lang


def reverse_relation(model, *parts):
    r"""
    Return the reverse of a relation to
    :class:`~translations.models.Translation` based on relation parts.

    :param model: the model to find the reverse relation for.
    :type model: ~translations.models.Translatable
    :param \*parts: the parts of the relation, already separated by
        :data:`~django.db.models.constants.LOOKUP_SEP` (usually ``__``)
    :type \*parts: list(str)
    :return: the reverse of the relation based on relation parts
    :rtpye: str
    :raise TypeError: if the model and relation combination is not
        translatable.
    """
    if parts:
        rel_field = model._meta.get_field(parts[0])
        rel_model = rel_field.related_model
        rel_reverse = rel_field.remote_field.name
        depth = reverse_relation(rel_model, *parts[1:])
        return '{}__{}'.format(depth, rel_reverse)
    else:
        if issubclass(model, translations.models.Translatable):
            trans_field = model._meta.get_field('translations')
            trans_query_name = trans_field.related_query_name()
            return trans_query_name
        else:
            raise TypeError(
                '{model} is not a `Translatable` type.'.format(
                    model=model
                )
            )


def get_relations_hierarchy(*relations):
    r"""
    Return a dict of first level relations as keys and their nested relations
    as values.

    >>> get_relations_hierarchy()
    {}
    >>> get_relations_hierarchy('countries')
    {'countries': []}
    >>> get_relations_hierarchy('countries__states')
    {'countries': ['states']}
    >>> get_relations_hierarchy(
    ... 'countries__states__cities',
    ... 'countries__states__villages',
    ... 'countries__phone_number',
    ... )
    {'countries': ['states__cities', 'states__villages', 'phone_number']}

    :param \*relations: a list of deeply nested relations to get their
        hierarchy.
    :type \*relations: list(str)
    :return: the first level relations and their nested relations.
    :rtype: dict(str, list(str))
    :raise ValueError: for invalid nested relations
    """
    hierarchy = {}

    for relation in relations:
        parts = relation.split(LOOKUP_SEP)

        if '' in parts:
            raise ValueError(
                '`{}` is not a valid relationship.'.format(
                    LOOKUP_SEP.join(parts)
                )
            )

        root = parts[0]
        nest = LOOKUP_SEP.join(parts[1:])

        hierarchy.setdefault(root, [])
        if nest:
            hierarchy[root].append(nest)

    return hierarchy


def get_translations(context, *relations, lang=None):
    r"""
    Return the translations of the context and its relations in a language.

    :param context: the context to translate
    :type context: ~django.db.models.query.QuerySet, ~django.db.models.Model
        or list(~django.db.models.Model)
    :param \*relations: a list of relations to fetch the translations for.
    :type \*relations: list(str)
    :param lang: the language of the translations to fetch, if ``None``
            is given the current active language will be used.
    :type lang: str or None
    :return: the translations
    :rtype: ~django.db.models.query.QuerySet
    """
    lang = get_validated_language(lang)

    # ------------ process context
    if isinstance(context, models.QuerySet):
        model = context.model
        filter_string = 'id__in'
        context_value = [instance.id for instance in context]
    elif isinstance(context, list):
        model = type(context[0])
        filter_string = 'id__in'
        context_value = [instance.id for instance in context]
    elif isinstance(context, models.Model):
        model = type(context)
        filter_string = 'id'
        context_value = context.id
    else:
        raise Exception('`context` is neither a model instance or a queryset or a list')

    # ------------ list of Q objects to perform Translation query on
    queries = []

    # ------------ query the translations for context itself
    if issubclass(model, translations.models.Translatable):
        queries.append(
            models.Q(**{
                '{}__{}'.format(
                    reverse_relation(model),
                    filter_string,
                ): context_value
            })
        )

    # ------------ query the translations for context relations
    for relation in relations:
        parts = relation.split(LOOKUP_SEP)

        if '' in parts:
            raise ValueError(
                '`{}` is not a valid relationship.'.format(
                    LOOKUP_SEP.join(parts)
                )
            )

        queries.append(
            models.Q(**{
                '{}__{}'.format(
                    reverse_relation(model, *parts),
                    filter_string,
                ): context_value
            })
        )

    # ------------ translations queryset
    queryset = translations.models.Translation.objects.filter(language=lang)

    # perform OR between Q objects
    if len(queries) > 0:
        filter_query = queries.pop()
        for query in queries:
            filter_query |= query
        queryset = queryset.filter(filter_query).distinct()
    else:
        queryset = translations.models.Translatable.objects.none()

    return queryset


def translate(context, *relations, lang=None, translations_queryset=None):
    lang = get_validated_language(lang)

    # ------------ process context
    if isinstance(context, models.QuerySet):
        model = context.model
        is_plural = True
    elif isinstance(context, list):
        model = type(context[0])
        is_plural = True
    elif isinstance(context, models.Model):
        model = type(context)
        is_plural = False
    else:
        raise Exception('`context` is neither a model instance or a queryset or a list')

    # ------------ generate translations queryset if none passed
    if translations_queryset is None:
        translations_queryset = get_translations(
            context,
            *relations,
            lang=lang
        )

    # ------------ convert translations queryset to dict for faster access
    if type(translations_queryset) != dict:
        translations_queryset = translations_queryset.select_related('content_type')
        translations_queryset_dict = {}
        for obj in translations_queryset:
            if obj.content_type.id not in translations_queryset_dict.keys():
                translations_queryset_dict[obj.content_type.id] = {}
            if obj.object_id not in translations_queryset_dict[obj.content_type.id].keys():
                translations_queryset_dict[obj.content_type.id][obj.object_id] = []
            translations_queryset_dict[obj.content_type.id][obj.object_id].append(obj)
        translations_queryset = translations_queryset_dict

    # ------------ translate context itself
    if issubclass(model, translations.models.Translatable):
        content_type = ContentType.objects.get_for_model(model)
        translatable_fields = model.get_translatable_fields()

        # translate obj function
        def translate_obj(obj):
            try:
                obj_translations = translations_queryset[content_type.id][str(obj.id)]
            except KeyError:
                pass
            else:
                for obj_translation in obj_translations:
                    field = model._meta.get_field(obj_translation.field)
                    if field in translatable_fields \
                            and hasattr(obj, obj_translation.field) \
                            and obj_translation.text:
                        setattr(obj, obj_translation.field, obj_translation.text)

        # translate based on plural/singular
        if is_plural:
            for obj in context:
                translate_obj(obj)
        else:
            translate_obj(context)

    # ------------ translate context relations
    relations_dict = get_relations_hierarchy(*relations)

    if len(relations_dict) > 0:
        # translate rel function
        def translate_rel(obj):
            for (relation_key, relation_descendants) in relations_dict.items():
                relation_value = getattr(obj, relation_key, None)
                if relation_value is not None:
                    if isinstance(relation_value, models.Manager):
                        relation_value = relation_value.all()
                    translate(
                        relation_value,
                        *relation_descendants,
                        lang=lang,
                        translations_queryset=translations_queryset
                    )

        # translate based on plural/singular
        if is_plural:
            for obj in context:
                translate_rel(obj)
        else:
            translate_rel(context)


def update_translations(context, lang=None):
    lang = get_validated_language(lang)

    # ------------ process context
    if isinstance(context, models.QuerySet):
        model = context.model
        is_plural = True
    elif isinstance(context, list):
        if len(context) > 0:
            model = type(context[0])
            is_plural = True
        else:
            return
    elif isinstance(context, models.Model):
        model = type(context)
        is_plural = False
    else:
        raise Exception('`context` is neither a model instance or a queryset or a list')

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
                if is_plural:
                    for obj in context:
                        add_translations(obj)
                else:
                    add_translations(context)

                if len(translations_objects) > 0:
                    translations.models.Translation.objects.bulk_create(translations_objects)
        except Exception:
            raise
