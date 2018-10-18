"""This module contains the context managers for the Translations app."""

from django.db import models

import translations.models
from translations.utils import _get_standard_language, \
    _get_relations_hierarchy, _get_purview, _get_translations


__docformat__ = 'restructuredtext'


class Context:
    """A context manager which provides custom translation functionalities."""

    def __init__(self, entity, *relations):
        """Initializes a `Context`."""
        hierarchy = _get_relations_hierarchy(*relations)
        self.mapping, self.query = _get_purview(entity, hierarchy)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def _get_changed_fields(self):
        """Yield the fields changed in the context."""
        for (ct_id, objs) in self.mapping.items():
            for (obj_id, obj) in objs.items():
                for field in type(obj)._get_translatable_fields_names():
                    text = getattr(obj, field, None)
                    default = obj._default_translatable_fields.get(field, None)
                    if text and text != default:
                        yield ({
                            'content_type_id': ct_id,
                            'object_id': obj_id,
                            'field': field,
                        }, text)

    def create(self, lang=None):
        """
        Create the translations from the context and write them to the
        database.
        """
        lang = _get_standard_language(lang)
        _translations = [
            translations.models.Translation(
                language=lang, text=text, **address
            ) for address, text in self._get_changed_fields()
        ]
        translations.models.Translation.objects.bulk_create(_translations)

    def read(self, lang=None):
        """
        Read the translations from the database and apply them on the context.
        """
        lang = _get_standard_language(lang)
        _translations = _get_translations(self.query, lang)
        for translation in _translations:
            ct_id = translation.content_type.id
            obj_id = translation.object_id
            field = translation.field
            text = translation.text
            obj = self.mapping[ct_id][obj_id]
            if field in type(obj)._get_translatable_fields_names():
                setattr(obj, field, text)

    def update(self, lang=None):
        """
        Update the translations from the context and write them to the
        database.
        """
        lang = _get_standard_language(lang)
        query = models.Q()
        _translations = []
        for address, text in self._get_changed_fields():
            query |= models.Q(**address)
            _translations.append(
                translations.models.Translation(
                    language=lang, text=text, **address
                )
            )
        translations.models.Translation.objects.filter(
            language=lang).filter(query).delete()
        translations.models.Translation.objects.bulk_create(_translations)

    def delete(self, lang=None):
        """
        Collect the translations from the context and delete them from the
        database.
        """
        lang = _get_standard_language(lang)
        _translations = _get_translations(self.query, lang)
        _translations.delete()

    def reset(self):
        """
        Reset the translations of the context to the original values.
        """
        for (ct_id, objs) in self.mapping.items():
            for (obj_id, obj) in objs.items():
                for (field, value) in obj._default_translatable_fields.items():
                    setattr(obj, field, value)
