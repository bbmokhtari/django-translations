*********
Languages
*********

.. module:: translations.languages

This module contains the languages for the Translations app.

.. function:: _get_supported_language(lang)

   Return the :term:`supported language` code of a custom language code.

   Searches the :data:`~django.conf.settings.LANGUAGES` in the settings for
   the custom language code, if the exact custom language code is found, it
   returns it, otherwise searches for the unaccented form of the custom
   language code, if the unaccented form of the custom language code is
   found, it returns it, otherwise it throws an error stating there is no
   such language supported in the settings.

   :param lang: The custom language code to derive
       the :term:`supported language` code out of.
   :type lang: str
   :return: The :term:`supported language` code derived out of
       the custom language code.
   :rtype: str
   :raise ValueError: If the language code is not specified in
       the :data:`~django.conf.settings.LANGUAGES` setting.

   Considering this setting:

   .. code-block:: python

      LANGUAGE_CODE = 'en-us'
      LANGUAGES = (
          ('en', 'English'),
          ('en-gb', 'English (Great Britain)'),
          ('de', 'German'),
          ('tr', 'Turkish'),
      )

   To get the :term:`supported language` code of a custom language code
   (an unaccented language code):

   .. testcode:: _get_supported_language

      from translations.languages import _get_supported_language

      # get the supported language
      custom = _get_supported_language('en')

      print(custom)

   .. testoutput:: _get_supported_language

      en

   To get the :term:`supported language` code of a custom language code
   (an existing accented language code):

   .. testcode:: _get_supported_language

      from translations.languages import _get_supported_language

      # get the supported language
      custom = _get_supported_language('en-gb')

      print(custom)

   .. testoutput:: _get_supported_language

      en-gb

   To get the :term:`supported language` code of a custom language code
   (a non-existing accented language code):

   .. testcode:: _get_supported_language

      from translations.languages import _get_supported_language

      # get the supported language
      custom = _get_supported_language('en-us')

      print(custom)

   .. testoutput:: _get_supported_language

      en

.. function:: _get_default_language()

   Return the :term:`supported language` code of the :term:`default language`
   code.

   :return: The :term:`supported language` code of
       the :term:`default language` code.
   :rtype: str
   :raise ValueError: If the :term:`default language` code is not supported.

   Considering this setting:

   .. code-block:: python

      LANGUAGE_CODE = 'en-us'
      LANGUAGES = (
          ('en', 'English'),
          ('en-gb', 'English (Great Britain)'),
          ('de', 'German'),
          ('tr', 'Turkish'),
      )

   To get the :term:`supported language` code of the :term:`default language`
   code:

   .. testcode:: _get_default_language

      from translations.languages import _get_default_language

      # get the default language
      default = _get_default_language()

      print(default)

   .. testoutput:: _get_default_language

      en

.. function:: _get_active_language()

   Return the :term:`supported language` code of the :term:`active language`
   code.

   :return: The :term:`supported language` code of
       the :term:`active language` code.
   :rtype: str
   :raise ValueError: If the :term:`active language` code is not supported.

   Considering this setting:

   .. code-block:: python

      LANGUAGE_CODE = 'en-us'
      LANGUAGES = (
          ('en', 'English'),
          ('en-gb', 'English (Great Britain)'),
          ('de', 'German'),
          ('tr', 'Turkish'),
      )

   To get the :term:`supported language` code of the :term:`active language`
   code:

   .. testcode:: _get_active_language

      from translations.languages import _get_active_language

      # get the active language
      active = _get_active_language()

      print(active)

   .. testoutput:: _get_active_language

      en

.. function:: _get_preferred_language(lang=None)

   Return the :term:`supported language` code of a preferred language code.

   If the preferred language code is passed in, it returns
   the :term:`supported language` code of it, otherwise it returns
   the :term:`supported language` code of the :term:`active language` code.

   :param lang: The preferred language code to get
       the :term:`supported language` code of.
       ``None`` means use the :term:`active language` code.
   :type lang: str or None
   :return: The :term:`supported language` code of the preferred language code.
   :rtype: str
   :raise ValueError: If the preferred language code is not supported.

   Considering this setting:

   .. code-block:: python

      LANGUAGE_CODE = 'en-us'
      LANGUAGES = (
          ('en', 'English'),
          ('en-gb', 'English (Great Britain)'),
          ('de', 'German'),
          ('tr', 'Turkish'),
      )

   To get the :term:`supported language` code of a preferred language code
   (no language code):

   .. testcode:: _get_preferred_language

      from translations.languages import _get_preferred_language

      # get the preferred language
      preferred = _get_preferred_language()

      print(preferred)

   .. testoutput:: _get_preferred_language

      en

   To get the :term:`supported language` code of a preferred language code
   (a custom language code):

   .. testcode:: _get_preferred_language

      from translations.languages import _get_preferred_language

      # get the preferred language
      preferred = _get_preferred_language('en-us')

      print(preferred)

   .. testoutput:: _get_preferred_language

      en

.. function:: _get_all_languages()

   Return all the :term:`supported language` codes.

   :return: The :term:`supported language` codes.
   :rtype: list(str)

   Considering this setting:

   .. code-block:: python

      LANGUAGE_CODE = 'en-us'
      LANGUAGES = (
          ('en', 'English'),
          ('en-gb', 'English (Great Britain)'),
          ('de', 'German'),
          ('tr', 'Turkish'),
      )

   To get all the :term:`supported language` codes:

   .. testcode:: _get_all_languages

      from translations.languages import _get_all_languages

      # get the supported languages
      languages = _get_all_languages()

      print(languages)

   .. testoutput:: _get_all_languages

      [
          'en',
          'en-gb',
          'de',
          'tr',
      ]

.. function:: _get_translation_language_choices()

   Return the :term:`translation language` choices.

   Returns the :term:`supported language` choices removing the
   :term:`default language` choice and adding an empty choice.

   :return: The :term:`translation language` choices.
   :rtype: list(tuple(str, str))
   :raise ValueError: If the :term:`default language` code is not supported.

   Considering this setting:

   .. code-block:: python

      LANGUAGE_CODE = 'en-us'
      LANGUAGES = (
          ('en', 'English'),
          ('en-gb', 'English (Great Britain)'),
          ('de', 'German'),
          ('tr', 'Turkish'),
      )

   To get the :term:`translation language` choices:

   .. testcode:: _get_translation_language_choices

      from translations.languages import _get_translation_language_choices

      # get the translation language choices
      choices = _get_translation_language_choices()

      print(choices)

   .. testoutput:: _get_translation_language_choices

      [
          (None, '---------'),
          ('en-gb', 'English (Great Britain)'),
          ('de', 'German'),
          ('tr', 'Turkish'),
      ]
