"""This module contains the forms for the Translations app."""

from django import forms

from translations.models import Translation


__docformat__ = 'restructuredtext'


def generate_translation_form(translatable):
    """Return a translation form based on a translatable model."""
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

    return TranslationForm
