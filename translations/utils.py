"""This module contains the utilities for the Translations app."""

from django.db import models
from django.db.models.query import prefetch_related_objects
from django.db.models.constants import LOOKUP_SEP
from django.core.exceptions import FieldError
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import get_language
from django.conf import settings

from translations.models import Translation, Translatable


__docformat__ = 'restructuredtext'


_standard_language_cache = {}
_translation_language_choices_cache = {}


def _get_standard_language(lang=None):
    """Return the standard language code of a custom language code."""
    lang = lang if lang else get_language()

    # check cache first
    try:
        return _standard_language_cache[lang]
    except KeyError:
        pass

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
        _standard_language_cache[lang] = lang
    elif code_exists:
        _standard_language_cache[lang] = code
    else:
        raise ValueError(
            'The language code `{}` is not supported.'.format(lang)
        )

    return _standard_language_cache[lang]


def _get_translation_language_choices():
    """Return the translation language choices."""
    default = _get_standard_language(settings.LANGUAGE_CODE)

    # check cache first
    try:
        return _translation_language_choices_cache[default]
    except KeyError:
        pass

    choices = [
        (None, '---------'),
    ]

    for language in settings.LANGUAGES:
        if language[0] != default:
            choices.append(language)

    _translation_language_choices_cache[default] = choices

    return _translation_language_choices_cache[default]


def _get_reverse_relation(model, relation):
    """Return the reverse of a model's relation."""
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


def _get_dissected_lookup(model, relation):
    dissected = {
        'relation': [],
        'field': '',
        'lookup': '',
        'translatable': False,
    }

    def _fill_dissected(model, *relation_parts):
        root = relation_parts[0]
        nest = relation_parts[1:]

        try:
            field = model._meta.get_field(root)
        except Exception as e:
            if not dissected['relation'] or nest or dissected['field']:
                raise e
            dissected['lookup'] = root
        else:
            field_model = field.related_model
            if field_model:
                dissected['relation'].append(root)
                if nest:
                    _fill_dissected(field_model, *nest)
            else:
                dissected['field'] = root
                if issubclass(model, Translatable):
                    if root in model._get_translatable_fields_names():
                        dissected['translatable'] = True
                if nest:
                    if len(nest) == 1:
                        dissected['lookup'] = nest[0]
                    else:
                        raise FieldError("Unsupported lookup '{}'".format(nest[0]))

    parts = relation.split(LOOKUP_SEP)

    _fill_dissected(model, *parts)

    return dissected


def _get_relations_hierarchy(*relations):
    """Return the `relations hierarchy` of some relations."""
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


def _get_entity_details(entity):
    """Return the iteration and type details of an entity."""
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


def _get_instance_groups(entity, hierarchy):
    """
    Return the `instance groups` of an entity and a `relations hierarchy` of
    it.
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
    """Return the translations of some `instance groups` in a language."""
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
