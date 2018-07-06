from django.db import models, transaction
from django.db.models.constants import LOOKUP_SEP
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import get_language
from django.conf import settings

import translations.models


def get_relations_dict(*relations):
    relations_dict = {}
    for relation in relations:
        parts = relation.split(LOOKUP_SEP)
        while True:
            try:
                parts.remove('')
            except ValueError:
                break
        if len(parts) > 0:
            base = parts.pop(0)
            if not relations_dict.get(base):
                relations_dict[base] = []
            if len(parts) > 0:
                relations_dict[base].append(LOOKUP_SEP.join(parts))
    return relations_dict


def get_iso_alpha_2_language_code(iso_alpha_2_language_code=None):
    iso_alpha_2_language_code = iso_alpha_2_language_code or get_language()

    if iso_alpha_2_language_code not in [language[0] for language in settings.LANGUAGES]:
        raise Exception("Language not supported")

    return iso_alpha_2_language_code


def get_translations(context, *relations, iso_alpha_2_language_code=None):
    iso_alpha_2_language_code = get_iso_alpha_2_language_code(iso_alpha_2_language_code)

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
    if issubclass(model, translations.models.TranslatableModel):
        related_query_name = model._meta.get_field('translations').related_query_name()
        queries.append(
            models.Q(**{'{}__{}'.format(related_query_name, filter_string): context_value})
        )

    # ------------ query the translations for context relations
    for relation in relations:
        base = model
        parts = relation.split(LOOKUP_SEP)

        # remove invalid relation parts
        while True:
            try:
                parts.remove('')
            except ValueError:
                break

        # generate related query name
        related_query_name_list = []
        for index, part in enumerate(parts):
            rel = base._meta.get_field(part)
            rel_model = rel.related_model
            related_query_name_list.append(rel.remote_field.name)
            if index == len(parts) - 1:
                if issubclass(rel_model, translations.models.TranslatableModel):
                    rel_related_query_name = rel_model._meta.get_field('translations').related_query_name()
                    related_query_name_list.append(rel_related_query_name)
                else:
                    break  # won't run else - so no queries will be appended cuz relation model is not translatable
            base = rel_model
        else:
            related_query_name_list.reverse()
            relation_related_query_name = LOOKUP_SEP.join(related_query_name_list)
            queries.append(
                models.Q(**{'{}__{}'.format(relation_related_query_name, filter_string): context_value})
            )

    # ------------ translations queryset
    queryset = translations.models.Translation.objects.filter(language=iso_alpha_2_language_code)

    # perform OR between Q objects
    if len(queries) > 0:
        filter_query = queries.pop()
        for query in queries:
            filter_query |= query
        queryset = queryset.filter(filter_query).distinct()
    else:
        queryset = translations.models.TranslatableModel.objects.none()

    return queryset


def translate(context, *relations, iso_alpha_2_language_code=None, translations_queryset=None):
    iso_alpha_2_language_code = get_iso_alpha_2_language_code(iso_alpha_2_language_code)

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
            iso_alpha_2_language_code=iso_alpha_2_language_code
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
    if issubclass(model, translations.models.TranslatableModel):
        content_type = ContentType.objects.get_for_model(model)
        translatable_fields = model.get_translatable_fields()

        # translate obj function
        def translate_obj(obj):
            try:
                obj_translations = translations_queryset[content_type.id][obj.id]
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
    relations_dict = get_relations_dict(*relations)

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
                        iso_alpha_2_language_code=iso_alpha_2_language_code,
                        translations_queryset=translations_queryset
                    )

        # translate based on plural/singular
        if is_plural:
            for obj in context:
                translate_rel(obj)
        else:
            translate_rel(context)


def renew_translations(context, iso_alpha_2_language_code=None):
    iso_alpha_2_language_code = get_iso_alpha_2_language_code(iso_alpha_2_language_code)

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
    if issubclass(model, translations.models.TranslatableModel):
        translatable_fields = model.get_translatable_fields()
        try:
            with transaction.atomic():
                # ------------ delete old translations
                translations_queryset = get_translations(
                    context,
                    iso_alpha_2_language_code=iso_alpha_2_language_code
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
                                    language=iso_alpha_2_language_code,
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
