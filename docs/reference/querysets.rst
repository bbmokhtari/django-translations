*********
QuerySets
*********

.. module:: translations.querysets

This module contains the querysets for the Translations app.

.. class:: TranslatableQuerySet

   A queryset which provides custom translation functionalities.

   .. method:: apply(self, lang=None)

      Apply a language to be used in the queryset.

      :param lang: The language to be used in the queryset.
          ``None`` means use the :term:`active language` code.
      :type lang: str or None
      :raise ValueError: If the language code is not included in
          the :data:`~django.conf.settings.LANGUAGES` setting.

   .. method:: all(self)

      Return the queryset.

   .. method:: filter(self, *args, **kwargs)

      Filter the queryset.
