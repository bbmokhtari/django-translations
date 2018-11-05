****************
Guide: Languages
****************

This module provides an in depth knowledge of the Translations languages.

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

What are languages?
===================

Translations provides some standard easy-to-access language codes out of the box.
Language codes like
the :term:`default language` code in the settings, or
the :term:`active language` code in the request, etc.

Translate Languages
===================

Translate languages are used in places like
the :doc:`Context <./context>`\ s and
the :ref:`translate <querysets.TranslatableQuerySet.translate>` method.

To access standard translate language codes use
the :data:`~translations.languages.translate` object.

To get the :term:`default language` code.

.. testcode:: _TRANSLATE.DEFAULT.1

   from translations.languages import translate

   # get the default language
   default = translate.DEFAULT

   print(default)

.. testoutput:: _TRANSLATE.DEFAULT.1

   en

To get the :term:`active language` code.
(assume ``en``)

.. testcode:: _TRANSLATE.ACTIVE.1

   from translations.languages import translate

   # get the active language
   active = translate.ACTIVE

   print(active)

.. testoutput:: _TRANSLATE.ACTIVE.1

   en

Probe Languages
===============

Probe languages are used in places like
the :ref:`TQ <query.TQ>`\ s and
the :ref:`probe <querysets.TranslatableQuerySet.probe>` method.

To access standard probe language codes use
the :data:`~translations.languages.probe` object.

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

To get the :term:`default language` code.

.. testcode:: _PROBE.DEFAULT.1

   from translations.languages import probe

   # get the default language
   default = probe.DEFAULT

   print(default)

.. testoutput:: _PROBE.DEFAULT.1

   en

To get the :term:`active language` code.
(assume ``en``)

.. testcode:: _PROBE.ACTIVE.1

   from translations.languages import probe

   # get the active language
   active = probe.ACTIVE

   print(active)

.. testoutput:: _PROBE.ACTIVE.1

   en

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
