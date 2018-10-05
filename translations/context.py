"""This module contains the context managers for the Translations app."""

from translations.models import Translation
from translations.utils import _get_standard_language, \
    _get_relations_hierarchy, _get_instance_groups, _get_translations


__docformat__ = 'restructuredtext'


class Context:
    """A context manager which provides custom translation functionalities."""

    def __init__(self, entity, *relations):
        """Initializes a `Context`."""
        hierarchy = _get_relations_hierarchy(*relations)
        self.groups = _get_instance_groups(entity, hierarchy)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def create(self, lang=None):
        """
        Create the translations from the context and write them to the
        database.
        """
        lang = _get_standard_language(lang)
        translations = []
        for (ct_id, objs) in self.groups.items():
            for (obj_id, obj) in objs.items():
                for field in type(obj)._get_translatable_fields_names():
                    text = getattr(obj, field, None)
                    default = obj._default_translatable_fields.get(field, None)
                    if text and text != default:
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
        """
        lang = _get_standard_language(lang)
        translations = _get_translations(self.groups, lang)
        for translation in translations:
            ct_id = translation.content_type.id
            obj_id = translation.object_id
            field = translation.field
            text = translation.text
            obj = self.groups[ct_id][obj_id]
            if field in type(obj)._get_translatable_fields_names():
                setattr(obj, field, text)

    def update(self, lang=None):
        """
        Update the translations from the context and write them to the
        database.
        """
        self.delete(lang)
        self.create(lang)

    def delete(self, lang=None):
        """
        Collect the translations from the context and delete them from the
        database.
        """
        lang = _get_standard_language(lang)
        translations = _get_translations(self.groups, lang)
        translations.delete()

    def reset(self):
        """
        Reset the translations of the context to the original values.
        """
        for (ct_id, objs) in self.groups.items():
            for (obj_id, obj) in objs.items():
                for (field, value) in obj._default_translatable_fields.items():
                    setattr(obj, field, value)
