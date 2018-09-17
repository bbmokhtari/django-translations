"""
This module contains the forms for the Translations app. It contains the
following members:

:func:`generate_translation_form`
    Return a translation form based on a translatable model.
"""

from django import forms

from .models import Translation


__docformat__ = 'restructuredtext'


def generate_translation_form(translatable):
    """
    Return a translation form based on a translatable model.

    Generates the translation form based on the translatable fields of the
    translatable model and returns it.

    :param translatable: The translatable model to generate the translation
        form based on.
    :type translatable: type(~translations.models.Translatable)
    :return: The translation form generated based on the translatable model.
    :rtype: type(~django.forms.ModelForm(~translations.models.Translation))
    """
    if not hasattr(translatable, '_cached_translation_form'):
        choices = translatable._get_translatable_fields_choices()

        class TranslationForm(forms.ModelForm):
            field = forms.ChoiceField(choices=choices)

            class Meta:
                model = Translation
                fields = (
                    'field',
                    'language',
                    'text',
                )

        translatable._cached_translation_form = TranslationForm

    return translatable._cached_translation_form
