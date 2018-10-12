"""This module contains the querysets for the Translations app."""

from django.db.models import query

from translations.utils import _get_standard_language, \
    _get_translations_lookup_query, _get_translations_query
from translations.context import Context


__docformat__ = 'restructuredtext'


class TranslatableQuerySet(query.QuerySet):
    """A queryset which provides custom translation functionalities."""

    def apply(self, *relations, lang=None, cipher=True):
        """Apply a language to be used in the queryset."""
        lang = _get_standard_language(lang)

        clone = self.all()

        # translations relations
        clone._translations_rels = relations
        # translations language
        clone._translations_lang = lang
        # whether the translation should happen or not
        clone._translations_do = cipher
        # whether the cache is translated
        clone._translations_translated = False

        return clone

    def all(self):
        """Return the queryset."""
        clone = super(TranslatableQuerySet, self).all()
        if hasattr(self, '_translations_rels'):
            clone._translations_rels = self._translations_rels
        if hasattr(self, '_translations_lang'):
            clone._translations_lang = self._translations_lang
        if hasattr(self, '_translations_do'):
            clone._translations_do = self._translations_do
        if hasattr(self, '_translations_translated'):
            clone._translations_translated = False  # reset the cache
        return clone

    def filter(self, *args, **kwargs):
        """Filter the queryset."""
        clone = self.all()
        if hasattr(clone, '_translations_lang') and clone._translations_do:
            queries = []
            for arg in args:
                queries.append(
                    _get_translations_query(
                        clone.model, arg, clone._translations_lang
                    )
                )
            for key, value in kwargs.items():
                queries.append(
                    _get_translations_lookup_query(
                        clone.model, key, value, clone._translations_lang
                    )
                )
            return super(TranslatableQuerySet, self).filter(*queries)
        else:
            return super(TranslatableQuerySet, self).filter(*args, **kwargs)

    def _translations_read(self):
        if hasattr(self, '_translations_lang') and self._translations_do:
            if not self._translations_translated:
                with Context(self._result_cache, *self._translations_rels) as context:
                    context.read(self._translations_lang)
                self._translations_translated = True

    def __getstate__(self):
        self._fetch_all()
        self._translations_read()
        return super(TranslatableQuerySet, self).__getstate__()

    def __len__(self):
        self._fetch_all()
        self._translations_read()
        return super(TranslatableQuerySet, self).__len__()

    def __iter__(self):
        self._fetch_all()
        self._translations_read()
        return super(TranslatableQuerySet, self).__iter__()

    def __bool__(self):
        self._fetch_all()
        self._translations_read()
        return super(TranslatableQuerySet, self).__bool__()

    def __getitem__(self, k):
        self._fetch_all()
        self._translations_read()
        return super(TranslatableQuerySet, self).__getitem__(k)

    def __repr__(self):
        self._fetch_all()
        self._translations_read()
        return super(TranslatableQuerySet, self).__repr__()
