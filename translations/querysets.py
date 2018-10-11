"""
This module contains the querysets for the Translations app. It contains the
following members:

:class:`TranslatableQuerySet`
    A queryset which provides custom translation functionalities.
"""

from django.db.models import query

from translations.utils import _get_standard_language


__docformat__ = 'restructuredtext'


class TranslatableQuerySet(query.QuerySet):
    """
    A queryset which provides custom translation functionalities.
    """

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
