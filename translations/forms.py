"""
This module contains the forms for the Translations app. It contains the
following members:

:func:`generate_translation_form`
    Return a translation form based on some choices.
"""
from django import forms

from .models import Translation


def generate_translation_form(choices):
    """
    Return a translation form based on some choices.

    Generates a translation form based on the given field choices and returns
    it.

    :param choices: The choices to generate the translation form based on.
    :type choices: list(tuple(str, str))
    :return: The translation form generated based on the choices.
    :rtype: ~django.forms.ModelForm(~translations.models.Translation)
    """
    class TranslationForm(forms.ModelForm):
        field = forms.ChoiceField(choices=choices)

        class Meta:
            model = Translation
            fields = (
                'field',
                'language',
                'text',
            )

    return TranslationForm
