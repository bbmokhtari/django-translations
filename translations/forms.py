from django import forms

from .models import Translation


def generate_translation_form(choices):
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
