"""This module contains the querysets for the Translations app."""

from django.db.models import query

from translations.utils import _get_standard_language, \
    _get_translations_lookup_query, _get_translations_query
from translations.context import Context


__docformat__ = 'restructuredtext'


class TranslatableQuerySet(query.QuerySet):
    """A queryset which provides custom translation functionalities."""

    def apply(self, *relations, lang=None):
        """Apply a language to be used in the queryset."""
        lang = _get_standard_language(lang)

        clone = self.all()

        # translations relations
        clone._translations_rels = relations
        # translations language
        clone._translations_lang = lang

        # whether the translation should happen or not
        clone._translations_cipher = True
        # whether the cache is translated
        clone._translations_translated = False

        return clone

    def cipher(self):
        clone = self.all()
        if hasattr(self, '_translations_cipher'):
            clone._translations_cipher = True
        return clone

    def decipher(self):
        clone = self.all()
        if hasattr(self, '_translations_cipher'):
            clone._translations_cipher = False
        return clone

    def filter(self, *args, **kwargs):
        """Filter the queryset."""
        if self._should_cipher():
            queries = self._get_translations_queries(*args, **kwargs)
            return super(TranslatableQuerySet, self).filter(*queries)
        else:
            return super(TranslatableQuerySet, self).filter(*args, **kwargs)

    def exclude(self, *args, **kwargs):
        """Exclude the queryset."""
        if self._should_cipher():
            queries = self._get_translations_queries(*args, **kwargs)
            return super(TranslatableQuerySet, self).exclude(*queries)
        else:
            return super(TranslatableQuerySet, self).exclude(*args, **kwargs)

    def _chain(self, **kwargs):
        clone = super(TranslatableQuerySet, self)._chain(**kwargs)

        if hasattr(self, '_translations_rels'):
            clone._translations_rels = self._translations_rels
        if hasattr(self, '_translations_lang'):
            clone._translations_lang = self._translations_lang
        if hasattr(self, '_translations_cipher'):
            clone._translations_cipher = self._translations_cipher
        if hasattr(self, '_translations_translated'):
            clone._translations_translated = False  # reset the cache

        return clone

    def _fetch_all(self):
        super(TranslatableQuerySet, self)._fetch_all()
        if self._should_cipher():
            if self._iterable_class is not query.ModelIterable:
                raise TypeError(
                    'Translations does not support this queryset.' + ' ' +
                    'If necessary you can `decipher` and then do it.'
                )
            if not self._translations_translated:
                with Context(self._result_cache, *self._translations_rels) as context:
                    context.read(self._translations_lang)
                self._translations_translated = True

    def _should_cipher(self):
        return hasattr(self, '_translations_lang') and self._translations_cipher

    def _get_translations_queries(self, *args, **kwargs):
        queries = []
        for arg in args:
            queries.append(
                _get_translations_query(
                    self.model, arg, self._translations_lang
                )
            )
        for key, value in kwargs.items():
            queries.append(
                _get_translations_lookup_query(
                    self.model, key, value, self._translations_lang
                )
            )
        return queries
