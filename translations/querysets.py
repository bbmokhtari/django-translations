"""
This module contains the querysets for the Translations app. It contains the
following members:

:class:`TranslatableQuerySet`
    A queryset which provides custom translation functionalities.
"""

from django.db.models import query

from translations.utils import _get_standard_language, \
    _get_translations_lookup_query, _get_translations_query
from translations.context import Context


__docformat__ = 'restructuredtext'


class TranslatableQuerySet(query.QuerySet):
    """
    A queryset which provides custom translation functionalities.
    """

    def all(self):
        clone = super(TranslatableQuerySet, self).all()
        if hasattr(self, '_applied_language'):
            clone._applied_language = self._applied_language
        return clone

    def apply(self, lang=None):
        """
        Applies a language to the queries.

        :param lang: The language to use in the queries.
            ``None`` means use the :term:`active language` code.
        :type lang: str or None
        :raise ValueError: If the language code is not included in
            the :data:`~django.conf.settings.LANGUAGES` setting.
        """
        lang = _get_standard_language(lang)
        clone = self.all()
        clone._applied_language = lang
        return clone

    def filter(self, *args, **kwargs):
        clone = self.all()
        if hasattr(clone, '_applied_language'):
            queries = []
            for arg in args:
                queries.append(_get_translations_query(clone.model, arg, clone._applied_language))
            for key, value in kwargs.items():
                queries.append(_get_translations_lookup_query(clone.model, key, value, clone._applied_language))
            return super(TranslatableQuerySet, self).filter(*queries)
        else:
            return super(TranslatableQuerySet, self).filter(*args, **kwargs)

    def translated(self, *relations):
        clone = self.all()
        if hasattr(clone, '_applied_language'):
            with Context(clone, *relations) as context:
                context.read(clone._applied_language)
                return clone
        else:
            return clone
