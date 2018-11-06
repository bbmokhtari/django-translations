from django.test import TestCase, override_settings

from translations.forms import generate_translation_form

from sample.models import Timezone, Continent, City


class GenerateTranslationFormTest(TestCase):

    def test_field_choices_automatic(self):
        form = generate_translation_form(City)
        self.assertListEqual(
            form.declared_fields['field'].choices,
            [(None, '---------'), ('name', 'Name'), ('denonym', 'Denonym')]
        )

    def test_field_choices_empty(self):
        form = generate_translation_form(Timezone)
        self.assertListEqual(
            form.declared_fields['field'].choices,
            [(None, '---------')]
        )

    def test_field_choices_explicit(self):
        form = generate_translation_form(Continent)
        self.assertListEqual(
            form.declared_fields['field'].choices,
            [(None, '---------'), ('name', 'Name'), ('denonym', 'Denonym')]
        )

    @override_settings(LANGUAGE_CODE='en-us')
    def test_nonexisting_accented_default_language_code(self):
        form = generate_translation_form(Continent)
        self.assertListEqual(
            form.declared_fields['language'].choices,
            [
                (None, '---------'),
                ('en-gb', 'English (Great Britain)'),
                ('de', 'German'),
                ('tr', 'Turkish')
            ]
        )

    @override_settings(LANGUAGE_CODE='en-gb')
    def test_existing_accented_default_language_code(self):
        form = generate_translation_form(Continent)
        self.assertListEqual(
            form.declared_fields['language'].choices,
            [
                (None, '---------'),
                ('en', 'English'),
                ('de', 'German'),
                ('tr', 'Turkish')
            ]
        )

    @override_settings(LANGUAGE_CODE='xx')
    def test_invalid_default_language_code(self):
        with self.assertRaises(OSError) as error:
            generate_translation_form(Continent)

        self.assertEqual(
            error.exception.args[0],
            'No translation files found for default language xx.'
        )
