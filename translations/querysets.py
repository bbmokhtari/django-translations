"""This module contains the querysets for the Translations app."""

from django.db.models import query

from translations.utils import _get_supported_language, \
    _get_default_language, _get_preferred_language
from translations.query import _fetch_translations_query_getter
from translations.context import Context


__docformat__ = 'restructuredtext'


class TranslatableQuerySet(query.QuerySet):
    """A queryset which provides custom translation functionalities."""

    def __init__(self, *args, **kwargs):
        """Initialize a `TranslatableQuerySet`."""
        super(TranslatableQuerySet, self).__init__(*args, **kwargs)
        self._trans_lang = _get_default_language()
        self._trans_quer = _get_default_language()
        self._trans_rels = ()
        self._trans_cache = False

    def _chain(self, **kwargs):
        """Return a copy of the current `TranslatableQuerySet`."""
        clone = super(TranslatableQuerySet, self)._chain(**kwargs)

        # default values for all
        clone._trans_lang = getattr(self, '_trans_lang')
        clone._trans_quer = getattr(self, '_trans_quer')
        clone._trans_rels = getattr(self, '_trans_rels')

        # reset cache on chaining
        clone._trans_cache = False

        return clone

    def _fetch_all(self):
        """Evaluate the `TranslatableQuerySet`."""
        super(TranslatableQuerySet, self)._fetch_all()

        if self._trans_lang == _get_default_language():
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

    def translate(self, lang=None):
        """Translate the `TranslatableQuerySet` in a language."""
        clone = self.all()
        clone._trans_lang = _get_preferred_language(lang)
        return clone

    def translate_related(self, *fields):
        """Translate some relations of the `TranslatableQuerySet`."""
        clone = self.all()
        clone._trans_rels = () if fields == (None,) else fields
        return clone

    def query_in(self, lang=None):
        """Query the `TranslatableQuerySet` in a language."""
        clone = self.all()
        if isinstance(lang, (list, tuple)):
            clone._trans_quer = [_get_supported_language(l) for l in lang]
        else:
            clone._trans_quer = _get_preferred_language(lang)
        return clone

    def filter(self, *args, **kwargs):
        """Filter the `TranslatableQuerySet` with lookups and queries."""
        query = _fetch_translations_query_getter(self.model, self._trans_quer)(*args, **kwargs)
        return super(TranslatableQuerySet, self).filter(query)

    def exclude(self, *args, **kwargs):
        """Exclude the `TranslatableQuerySet` with lookups and queries."""
        query = _fetch_translations_query_getter(self.model, self._trans_quer)(*args, **kwargs)
        return super(TranslatableQuerySet, self).exclude(query)
