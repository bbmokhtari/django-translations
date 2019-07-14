"""This module contains the utilities for the Translations app."""

from django.db import models
from django.db.models.query import prefetch_related_objects
from django.db.models.constants import LOOKUP_SEP
from django.core.exceptions import FieldError
from django.contrib.contenttypes.models import ContentType
from django.utils.functional import SimpleLazyObject

import translations.models


__docformat__ = 'restructuredtext'


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


def _get_dissected_lookup(model, lookup):
    """Return the dissected info of a lookup."""
    dissected = {
        'relation': [],
        'field': '',
        'supplement': '',
        'translatable': False,
    }

    def _fill_dissected(model, *relation_parts):
        root = relation_parts[0]
        nest = relation_parts[1:]

        try:
            if root == 'pk':
                field = model._meta.pk
            else:
                field = model._meta.get_field(root)
        except Exception as e:
            if not dissected['relation'] or nest or dissected['field']:
                raise e
            dissected['supplement'] = root
        else:
            field_model = field.related_model
            if field_model:
                dissected['relation'].append(root)
                if nest:
                    _fill_dissected(field_model, *nest)
            else:
                dissected['field'] = root
                if issubclass(model, translations.models.Translatable):
                    if root in model._get_translatable_fields_names():
                        dissected['translatable'] = True
                if nest:
                    if len(nest) == 1:
                        dissected['supplement'] = nest[0]
                    else:
                        raise FieldError("Unsupported lookup '{}'".format(
                            nest[0])
                        )

    parts = lookup.split(LOOKUP_SEP)

    _fill_dissected(model, *parts)

    return dissected


def _get_relations_hierarchy(*relations):
    """Return the relations hierarchy of some relations."""
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

    error_message = SimpleLazyObject(
        lambda: '`{}` is neither {} nor {}.'.format(
            entity,
            'a model instance',
            'an iterable of model instances',
        )
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


def _get_purview(entity, hierarchy):
    """Return the purview of an entity and a relations hierarchy of it."""
    mapping = {}
    query = models.Q()

    def _fill_entity(entity, hierarchy, included=True):
        iterable, model = _get_entity_details(entity)

        if model is None:
            return

        content_type_id = ContentType.objects.get_for_model(model).id

        if included:
            instances = mapping.setdefault(content_type_id, {})
            if not issubclass(model, translations.models.Translatable):
                raise TypeError('`{}` is not Translatable!'.format(model))

        def _fill_obj(obj):
            if included:
                if not hasattr(obj, '_default_translatable_fields'):
                    obj._default_translatable_fields = {
                        field: getattr(obj, field) for field in
                        type(obj)._get_translatable_fields_names()
                    }
                object_id = str(obj.pk)
                instances[object_id] = obj
                nonlocal query
                query |= models.Q(
                    content_type__id=content_type_id,
                    object_id=object_id,
                )

            if hierarchy:
                for (relation, detail) in hierarchy.items():
                    value = getattr(obj, relation, None)

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

    return mapping, query


def _get_translations(query, lang):
    """Return the `Translation` queryset of a query in a language."""
    if (query):
        queryset = translations.models.Translation.objects.filter(
            language=lang,
        ).filter(
            query,
        ).select_related('content_type')

        return queryset
    else:
        return translations.models.Translation.objects.none()
