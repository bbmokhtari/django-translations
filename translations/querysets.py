"""This module contains the querysets for the Translations app."""

from django.db.models import query

from translations.utils import _get_standard_language, \
    _get_translations_lookup_query, _get_translations_query


__docformat__ = 'restructuredtext'


class TranslatableQuerySet(query.QuerySet):
    """A queryset which provides custom translation functionalities."""

    def apply(self, lang=None):
        """Apply a language to be used in the queryset."""
        lang = _get_standard_language(lang)
        clone = self.all()
        clone._applied_language = lang
        return clone

    def all(self):
        """Return the queryset."""
        clone = super(TranslatableQuerySet, self).all()
        if hasattr(self, '_applied_language'):
            clone._applied_language = self._applied_language
        return clone

    def filter(self, *args, **kwargs):
        """Filter the queryset."""
        clone = self.all()
        if hasattr(clone, '_applied_language'):
            queries = []
            for arg in args:
                queries.append(
                    _get_translations_query(
                        clone.model, arg, clone._applied_language
                    )
                )
            for key, value in kwargs.items():
                queries.append(
                    _get_translations_lookup_query(
                        clone.model, key, value, clone._applied_language
                    )
                )
            return super(TranslatableQuerySet, self).filter(*queries)
        else:
            return super(TranslatableQuerySet, self).filter(*args, **kwargs)
