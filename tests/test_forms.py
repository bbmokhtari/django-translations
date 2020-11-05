from django.test import TestCase, override_settings

from translations.forms import generate_translation_form

from sample.models import Timezone, Continent, City


class GenerateTranslationFormTest(TestCase):

    def test_field_choices_automatic(self):
        """
        Determine the translation fields to use of - fields list.

        Args:
            self: (todo): write your description
        """
        form = generate_translation_form(City)
        self.assertListEqual(
            form.declared_fields['field'].choices,
            [(None, '---------'), ('name', 'Name'), ('denonym', 'Denonym')]
        )

    def test_field_choices_empty(self):
        """
        Determine empty list of choices.

        Args:
            self: (todo): write your description
        """
        form = generate_translation_form(Timezone)
        self.assertListEqual(
            form.declared_fields['field'].choices,
            [(None, '---------')]
        )

    def test_field_choices_explicit(self):
        """
        Returns a list of choices of the default choices.

        Args:
            self: (todo): write your description
        """
        form = generate_translation_form(Continent)
        self.assertListEqual(
            form.declared_fields['field'].choices,
            [(None, '---------'), ('name', 'Name'), ('denonym', 'Denonym')]
        )

    @override_settings(LANGUAGE_CODE='en-us')
    def test_nonexisting_accented_default_language_code(self):
        """
        Generate default language.

        Args:
            self: (todo): write your description
        """
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
        """
        Test if language language language.

        Args:
            self: (todo): write your description
        """
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
        """
        Set the default language code.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(OSError) as error:
            generate_translation_form(Continent)

        self.assertEqual(
            error.exception.args[0],
            'No translation files found for default language xx.'
        )
