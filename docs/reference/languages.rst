**************
Ref: Languages
**************

.. module:: translations.languages

This module contains the languages for the Translations app.

.. important::

   The examples are assumed to be executed using these settings.

   .. code-block:: python

      LANGUAGE_CODE = 'en-us'
      LANGUAGES = (
          ('en', 'English'),
          ('en-gb', 'English (Great Britain)'),
          ('de', 'German'),
          ('tr', 'Turkish'),
      )

   Please keep these settings in mind in order to understand the examples better.

.. function:: _get_supported_language(lang)

   Return the :term:`supported language` code of a custom language code.

   Searches the :data:`~django.conf.settings.LANGUAGES` in the settings for
   the custom language code, if the exact custom language code is found, it
   returns it, otherwise searches for the unaccented form of the custom
   language code, if the unaccented form of the custom language code is
   found, it returns it, otherwise it throws an error stating there is no
   such language supported in the settings.

   :param lang: The custom language code to get
       the :term:`supported language` code of.
   :type lang: str
   :return: The :term:`supported language` code of the custom language code.
   :rtype: str
   :raise ValueError: If the language code is not specified in
       the :data:`~django.conf.settings.LANGUAGES` setting.

   To get the :term:`supported language` code of a custom language code
   (an unaccented language code):

   .. testcode:: _get_supported_language.1

      from translations.languages import _get_supported_language

      # get the supported language
      custom = _get_supported_language('en')

      print(custom)

   .. testoutput:: _get_supported_language.1

      en

   To get the :term:`supported language` code of a custom language code
   (an existing accented language code):

   .. testcode:: _get_supported_language.2

      from translations.languages import _get_supported_language

      # get the supported language
      custom = _get_supported_language('en-gb')

      print(custom)

   .. testoutput:: _get_supported_language.2

      en-gb

   To get the :term:`supported language` code of a custom language code
   (a non-existing accented language code):

   .. testcode:: _get_supported_language.3

      from translations.languages import _get_supported_language

      # get the supported language
      custom = _get_supported_language('en-us')

      print(custom)

   .. testoutput:: _get_supported_language.3

      en

.. function:: _get_default_language()

   Return the :term:`supported language` code of the :term:`default language`
   code.

   :return: The :term:`supported language` code of
       the :term:`default language` code.
   :rtype: str
   :raise ValueError: If the :term:`default language` code is not supported.

   To get the :term:`supported language` code of the :term:`default language`
   code:

   .. testcode:: _get_default_language.1

      from translations.languages import _get_default_language

      # get the default language
      default = _get_default_language()

      print(default)

   .. testoutput:: _get_default_language.1

      en

.. function:: _get_active_language()

   Return the :term:`supported language` code of the :term:`active language`
   code.

   :return: The :term:`supported language` code of
       the :term:`active language` code.
   :rtype: str
   :raise ValueError: If the :term:`active language` code is not supported.

   To get the :term:`supported language` code of the :term:`active language`
   code
   (assume ``en``):

   .. testcode:: _get_active_language.1

      from translations.languages import _get_active_language

      # get the active language
      active = _get_active_language()

      print(active)

   .. testoutput:: _get_active_language.1

      en

.. function:: _get_all_languages()

   Return all the :term:`supported language` codes.

   :return: All the :term:`supported language` codes.
   :rtype: list(str)

   To get all the :term:`supported language` codes:

   .. testcode:: _get_all_languages.1

      from translations.languages import _get_all_languages

      # get all the languages
      languages = _get_all_languages()

      print(languages)

   .. testoutput:: _get_all_languages.1

      [
          'en',
          'en-gb',
          'de',
          'tr',
      ]

.. function:: _get_all_choices()

   Return all the :term:`supported language` choices.

   :return: All the :term:`supported language` choices.
   :rtype: list(tuple(str, str))

   To get all the :term:`supported language` choices:

   .. testcode:: _get_all_choices.1

      from translations.languages import _get_all_choices

      # get all the language choices
      choices = _get_all_choices()

      print(choices)

   .. testoutput:: _get_all_choices.1

      [
          (None, '---------'),
          ('en', 'English'),
          ('en-gb', 'English (Great Britain)'),
          ('de', 'German'),
          ('tr', 'Turkish'),
      ]

.. function:: _get_translation_languages()

   Return the :term:`translation language` codes.

   :return: The :term:`translation language` codes.
   :rtype: list(str)

   To get the :term:`translation language` codes:

   .. testcode:: _get_translation_languages.1

      from translations.languages import _get_translation_languages

      # get the translation languages
      languages = _get_translation_languages()

      print(languages)

   .. testoutput:: _get_translation_languages.1

      [
          'en-gb',
          'de',
          'tr',
      ]

.. function:: _get_translation_choices()

   Return the :term:`translation language` choices.

   :return: The :term:`translation language` choices.
   :rtype: list(tuple(str, str))
   :raise ValueError: If the :term:`default language` code is not supported.

   To get the :term:`translation language` choices:

   .. testcode:: _get_translation_choices.1

      from translations.languages import _get_translation_choices

      # get the translation language choices
      choices = _get_translation_choices()

      print(choices)

   .. testoutput:: _get_translation_choices.1

      [
          (None, '---------'),
          ('en-gb', 'English (Great Britain)'),
          ('de', 'German'),
          ('tr', 'Turkish'),
      ]

.. function:: _get_translate_language(lang=None)

   Return the :term:`supported language` code of a translate language code.

   If the translate language code is passed in, it returns
   the :term:`supported language` code of it, otherwise it returns
   the :term:`supported language` code of the :term:`active language` code.

   :param lang: The translate language code to get
       the :term:`supported language` code of.
       ``None`` means use the :term:`active language` code.
   :type lang: str or None
   :return: The :term:`supported language` code of the translate language code.
   :rtype: str
   :raise ValueError: If the translate language code is not supported.

   To get the :term:`supported language` code of a translate language code
   (the :term:`active language` code - assume ``en``):

   .. testcode:: _get_translate_language.1

      from translations.languages import _get_translate_language

      # get the translate language
      translate = _get_translate_language()

      print(translate)

   .. testoutput:: _get_translate_language.1

      en

   To get the :term:`supported language` code of a translate language code
   (a custom language code):

   .. testcode:: _get_translate_language.2

      from translations.languages import _get_translate_language

      # get the translate language
      translate = _get_translate_language('en-us')

      print(translate)

   .. testoutput:: _get_translate_language.2

      en

.. function:: _get_probe_language(lang=None)

   Return the :term:`supported language` code(s) of some probe language code(s).

   If the probe language code(s) is (are) passed in, it returns
   the :term:`supported language` code(s) of it (them), otherwise it returns
   the :term:`supported language` code of the :term:`active language` code.

   :param lang: The probe language code(s) to get
       the :term:`supported language` code(s) of.
       ``None`` means use the :term:`active language` code.
   :type lang: str or list or None
   :return: The :term:`supported language` code(s) of the probe language code(s).
   :rtype: str
   :raise ValueError: If the probe language code(s) is (are) not supported.

   To get the :term:`supported language` code(s) of some probe language code(s)
   (the :term:`active language` code - assume ``en``):

   .. testcode:: _get_probe_language.1

      from translations.languages import _get_probe_language

      # get the probe language
      probe = _get_probe_language()

      print(probe)

   .. testoutput:: _get_probe_language.1

      en

   To get the :term:`supported language` code(s) of some probe language code(s)
   (a custom language code):

   .. testcode:: _get_probe_language.2

      from translations.languages import _get_probe_language

      # get the probe language
      probe = _get_probe_language('en-us')

      print(probe)

   .. testoutput:: _get_probe_language.2

      en

   To get the :term:`supported language` code(s) of some probe language code(s)
   (multiple custom language codes):

   .. testcode:: _get_probe_language.3

      from translations.languages import _get_probe_language

      # get the probe language
      probe = _get_probe_language(['en-us', 'en-gb'])

      print(probe)

   .. testoutput:: _get_probe_language.3

      [
          'en',
          'en-gb',
      ]

.. class:: _TRANSLATE

   A class which provides standard translate language codes.

   .. attribute:: DEFAULT

      Return the :term:`default language` code.

      To get the :term:`default language` code.

      .. testcode:: _TRANSLATE.DEFAULT.1

         from translations.languages import translate

         # get the default language
         default = translate.DEFAULT

         print(default)

      .. testoutput:: _TRANSLATE.DEFAULT.1

         en

   .. attribute:: ACTIVE

      Return the :term:`active language` code.

      To get the :term:`active language` code.
      (assume ``en``)

      .. testcode:: _TRANSLATE.ACTIVE.1

         from translations.languages import translate

         # get the active language
         active = translate.ACTIVE

         print(active)

      .. testoutput:: _TRANSLATE.ACTIVE.1

         en

.. class:: _PROBE

   A class which provides standard probe language codes.

   .. attribute:: DEFAULT

      Return the :term:`default language` code.

      To get the :term:`default language` code.

      .. testcode:: _PROBE.DEFAULT.1

         from translations.languages import probe

         # get the default language
         default = probe.DEFAULT

         print(default)

      .. testoutput:: _PROBE.DEFAULT.1

         en

   .. attribute:: ACTIVE

      Return the :term:`active language` code.

      To get the :term:`active language` code.
      (assume ``en``)

      .. testcode:: _PROBE.ACTIVE.1

         from translations.languages import probe

         # get the active language
         active = probe.ACTIVE

         print(active)

      .. testoutput:: _PROBE.ACTIVE.1

         en

   .. attribute:: DEFAULT_ACTIVE

      Return the :term:`default language` and :term:`active language` codes.

      .. testsetup:: _PROBE.DEFAULT_ACTIVE.1

         from django.utils.translation import activate

         activate('en')

      .. testcleanup:: _PROBE.DEFAULT_ACTIVE.1

         from django.utils.translation import deactivate

         deactivate()

      .. testsetup:: _PROBE.DEFAULT_ACTIVE.2

         from django.utils.translation import activate

         activate('de')

      .. testcleanup:: _PROBE.DEFAULT_ACTIVE.2

         from django.utils.translation import deactivate

         deactivate()

      To get the :term:`default language` and :term:`active language` codes.
      (assume ``en``)

      .. testcode:: _PROBE.DEFAULT_ACTIVE.1

         from translations.languages import probe

         # get the default and active language
         defact = probe.DEFAULT_ACTIVE

         print(defact)

      .. testoutput:: _PROBE.DEFAULT_ACTIVE.1

         en

      To get the :term:`default language` and :term:`active language` codes.
      (assume ``de``)

      .. testcode:: _PROBE.DEFAULT_ACTIVE.2

         from translations.languages import probe

         # get the default and active language
         defact = probe.DEFAULT_ACTIVE

         print(defact)

      .. testoutput:: _PROBE.DEFAULT_ACTIVE.2

         [
             'en',
             'de',
         ]

   .. attribute:: TRANSLATION

      Return the :term:`translation language` codes.

      To get the :term:`translation language` codes.

      .. testcode:: _PROBE.TRANSLATION.1

         from translations.languages import probe

         # get the translation language
         translation = probe.TRANSLATION

         print(translation)

      .. testoutput:: _PROBE.TRANSLATION.1

         [
             'en-gb',
             'de',
             'tr',
         ]

   .. attribute:: ALL

      Return all the :term:`supported language` codes.

      To get all the :term:`supported language` codes.

      .. testcode:: _PROBE.ALL.1

         from translations.languages import probe

         # get all the language
         all = probe.ALL

         print(all)

      .. testoutput:: _PROBE.ALL.1

         [
             'en',
             'en-gb',
             'de',
             'tr',
         ]

.. data:: translate

   An object which provides standard translate language codes.

   An instance of :class:`_TRANSLATE`

.. data:: probe

   An object which provides standard probe language codes.

   An instance of :class:`_PROBE`
