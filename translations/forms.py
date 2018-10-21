"""This module contains the form utilities for the Translations app."""

from django import forms

from translations.models import Translation
from translations.utils import _get_translation_language_choices


__docformat__ = 'restructuredtext'


def generate_translation_form(translatable):
    """
    Return a `Translation` form based on a `Translatable` model and
    the `translation language`\ s.
    """
    fields = translatable._get_translatable_fields_choices()
    languages = _get_translation_language_choices()

    class TranslationForm(forms.ModelForm):
        field = forms.ChoiceField(choices=fields)
        language = forms.ChoiceField(choices=languages)

        class Meta:
            model = Translation
            fields = (
                'field',
                'language',
                'text',
            )

    return TranslationForm
