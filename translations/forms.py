"""This module contains the forms for the Translations app."""

from django import forms
from django.conf import settings

from translations.models import Translation
from translations.utils import _get_standard_language


__docformat__ = 'restructuredtext'


def generate_translation_form(translatable):
    """Return a translation form based on a translatable model."""
    fields = translatable._get_translatable_fields_choices()
    default = _get_standard_language(settings.LANGUAGE_CODE)
    languages = [lang for lang in settings.LANGUAGES if lang[0] != default]

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
