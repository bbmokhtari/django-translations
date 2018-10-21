*****
Forms
*****

.. module:: translations.forms

This module contains the forms for the Translations app.

.. function:: generate_translation_form(translatable)

   Return a :class:`~translations.models.Translation` form based on
   a :class:`~translations.models.Translatable` model and
   the :term:`translation language`\ s.

   Generates the :class:`~translations.models.Translation` form based on
   the translatable fields of the :class:`~translations.models.Translatable`
   model and the :term:`translation language`\ s and returns it.

   :param translatable: The :class:`~translations.models.Translatable` model to
       generate the :class:`~translations.models.Translation` form based on.
   :type translatable: type(~translations.models.Translatable)
   :return: The :class:`~translations.models.Translation` form generated based
       on the :class:`~translations.models.Translatable` model and
       the :term:`translation language`\ s.
   :rtype: type(~django.forms.ModelForm(~translations.models.Translation))
   :raise ValueError: If the :term:`default language` code is not supported.

   To get a :class:`~translations.models.Translation` form based on
   a :class:`~translations.models.Translatable` model and
   the :term:`translation language`\ s:

   .. testcode:: generate_translation_form

      from translations.forms import generate_translation_form
      from sample.models import Continent

      # get the translation form based on the translatable model
      # and the translation language
      form = generate_translation_form(Continent)

      print(form.declared_fields['field'].choices)
      print(form.declared_fields['language'].choices)

   .. testoutput:: generate_translation_form

      [
          (None, '---------'),
          ('name', 'name'),
          ('denonym', 'denonym'),
      ]
      [
          (None, '---------'),
          ('en-gb', 'English (Great Britain)'),
          ('de', 'German'),
          ('tr', 'Turkish'),
      ]
