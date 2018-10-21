*****
Forms
*****

.. module:: translations.forms

This module contains the forms for the Translations app.

.. function:: generate_translation_form(translatable)

   Return a translation form based on a translatable model.

   Generates the translation form based on the translatable fields of the
   translatable model and returns it.

   :param translatable: The translatable model to generate the translation
       form based on.
   :type translatable: type(~translations.models.Translatable)
   :return: The translation form generated based on the translatable model.
   :rtype: type(~django.forms.ModelForm(~translations.models.Translation))

   To get a translation form based on a translatable model:

   .. testcode:: generate_translation_form

      from translations.forms import generate_translation_form
      from sample.models import Continent

      # get the translation form based on the translatable model 
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
