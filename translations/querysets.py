"""This module contains the querysets for the Translations app."""

from django.db.models import query

from translations.utils import _get_standard_language, \
    _get_translations_query_of_lookup, _get_translations_query_of_query
from translations.context import Context


__docformat__ = 'restructuredtext'


class TranslatableQuerySet(query.QuerySet):
    """A queryset which provides custom translation functionalities."""

    def _chain(self, **kwargs):
        """Return a translatable chained queryset."""
        clone = super(TranslatableQuerySet, self)._chain(**kwargs)

        # default values for all
        clone._trans_lang = getattr(self, '_trans_lang', None)
        clone._trans_rels = getattr(self, '_trans_rels', ())
        clone._trans_cipher = getattr(self, '_trans_cipher', True)
        clone._trans_cache = False

        return clone

    def _fetch_all(self):
        """Evaluate the queryset."""
        super(TranslatableQuerySet, self)._fetch_all()

        if not (self._trans_lang and self._trans_cipher):
            return

        if self._iterable_class is not query.ModelIterable:
            raise TypeError(
                'Translations does not support custom iteration (yet). ' +
                'e.g. values, values_list, etc. ' +
                'If necessary you can `decipher` and then do it.'
            )

        if not self._trans_cache:
            with Context(self._result_cache, *self._trans_rels) \
                    as context:
                context.read(self._trans_lang)
            self._trans_cache = True

    def _get_translations_queries(self, *args, **kwargs):
        """Return the translations queries of lookups and queries."""
        if not (self._trans_lang and self._trans_cipher):
            return []

        queries = []

        for arg in args:
            queries.append(
                _get_translations_query_of_query(
                    self.model, arg, self._trans_lang)
            )

        for key, value in kwargs.items():
            queries.append(
                _get_translations_query_of_lookup(
                    self.model, key, value, self._trans_lang)
            )

        return queries

    def apply(self, lang=None):
        """Apply a language to be used in the queryset."""
        clone = self.all()
        clone._trans_lang = _get_standard_language(lang)
        return clone

    def translate_related(*fields):
        """Translate some relations of the queryset."""
        clone = self.all()
        clone._trans_rels = () if fields == (None,) else fields
        return clone

    def cipher(self):
        """Use the applied language in the queryset."""
        clone = self.all()
        clone._trans_cipher = True
        return clone

    def decipher(self):
        """Use the default language in the queryset."""
        clone = self.all()
        clone._trans_cipher = False
        return clone

    def filter(self, *args, **kwargs):
        """Filter the queryset with lookups and queries."""
        queries = self._get_translations_queries(*args, **kwargs)
        if queries:
            return super(TranslatableQuerySet, self).filter(*queries)
        else:
            return super(TranslatableQuerySet, self).filter(*args, **kwargs)

    def exclude(self, *args, **kwargs):
        """Exclude the queryset with lookups and queries."""
        queries = self._get_translations_queries(*args, **kwargs)
        if queries:
            return super(TranslatableQuerySet, self).exclude(*queries)
        else:
            return super(TranslatableQuerySet, self).exclude(*args, **kwargs)
