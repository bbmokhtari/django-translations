from django.test import TestCase, override_settings
from django.utils.translation import override

from translations.languages import _get_supported_language, \
    _get_default_language, _get_active_language, _get_preferred_language, \
    _get_all_languages, _get_translation_language_choices


class GetsupportedLanguageTest(TestCase):
    """Tests for `_get_supported_language`."""

    def test_unaccented(self):
        self.assertEqual(
            _get_supported_language('en'),
            'en'
        )

    def test_nonexisting_accented(self):
        self.assertEqual(
            _get_supported_language('en-us'),
            'en'
        )

    def test_existing_accented(self):
        self.assertEqual(
            _get_supported_language('en-gb'),
            'en-gb'
        )

    def test_invalid(self):
        with self.assertRaises(ValueError) as error:
            _get_supported_language('xx')

        self.assertEqual(
            error.exception.args[0],
            'The language code `xx` is not supported.'
        )


class GetDefaultLanguageTest(TestCase):
    """Tests for `_get_default_language`."""

    @override_settings(LANGUAGE_CODE='en')
    def test_unaccented(self):
        self.assertEqual(
            _get_default_language(),
            'en'
        )

    @override_settings(LANGUAGE_CODE='en-us')
    def test_nonexisting_accented(self):
        self.assertEqual(
            _get_default_language(),
            'en'
        )

    @override_settings(LANGUAGE_CODE='en-gb')
    def test_existing_accented(self):
        self.assertEqual(
            _get_default_language(),
            'en-gb'
        )

    @override_settings(LANGUAGE_CODE='xx')
    def test_invalid(self):
        with self.assertRaises(ValueError) as error:
            _get_default_language()

        self.assertEqual(
            error.exception.args[0],
            'The language code `xx` is not supported.'
        )


class GetActiveLanguageTest(TestCase):
    """Tests for `_get_active_language`."""

    @override(language='en', deactivate=True)
    def test_unaccented(self):
        self.assertEqual(
            _get_active_language(),
            'en'
        )

    @override(language='en-us', deactivate=True)
    def test_nonexisting_accented(self):
        self.assertEqual(
            _get_active_language(),
            'en'
        )

    @override(language='en-gb', deactivate=True)
    def test_existing_accented(self):
        self.assertEqual(
            _get_active_language(),
            'en-gb'
        )

    @override(language='xx', deactivate=True)
    def test_invalid(self):
        with self.assertRaises(ValueError) as error:
            _get_active_language()

        self.assertEqual(
            error.exception.args[0],
            'The language code `xx` is not supported.'
        )


class GetPreferredLanguageTest(TestCase):
    """Tests for `_get_preferred_language`."""

    @override(language='en', deactivate=True)
    def test_unaccented_active(self):
        self.assertEqual(
            _get_preferred_language(),
            'en'
        )

    @override(language='en-us', deactivate=True)
    def test_nonexisting_accented_active(self):
        self.assertEqual(
            _get_preferred_language(),
            'en'
        )

    @override(language='en-gb', deactivate=True)
    def test_existing_accented_active(self):
        self.assertEqual(
            _get_preferred_language(),
            'en-gb'
        )

    @override(language='xx', deactivate=True)
    def test_invalid_active(self):
        with self.assertRaises(ValueError) as error:
            _get_preferred_language()

        self.assertEqual(
            error.exception.args[0],
            'The language code `xx` is not supported.'
        )

    def test_unaccented_custom(self):
        self.assertEqual(
            _get_preferred_language('en'),
            'en'
        )

    def test_nonexisting_accented_custom(self):
        self.assertEqual(
            _get_preferred_language('en-us'),
            'en'
        )

    def test_existing_accented_custom(self):
        self.assertEqual(
            _get_preferred_language('en-gb'),
            'en-gb'
        )

    def test_invalid_custom(self):
        with self.assertRaises(ValueError) as error:
            _get_preferred_language('xx')

        self.assertEqual(
            error.exception.args[0],
            'The language code `xx` is not supported.'
        )


class GetAllLanguages(TestCase):
    """Tests for `_get_all_languages`."""

    def test_get_all_languages(self):
        languages = _get_all_languages()
        self.assertListEqual(
            languages,
            [
                'en',
                'en-gb',
                'de',
                'tr',
            ]
        )


class GetTranslationLanguageChoicesTest(TestCase):
    """Tests for `_get_translation_language_choices`."""

    @override_settings(LANGUAGE_CODE='en-us')
    def test_nonexisting_accented_default_language_code(self):
        self.assertListEqual(
            _get_translation_language_choices(),
            [
                (None, '---------'),
                ('en-gb', 'English (Great Britain)'),
                ('de', 'German'),
                ('tr', 'Turkish')
            ]
        )

    @override_settings(LANGUAGE_CODE='en-gb')
    def test_existing_accented_default_language_code(self):
        self.assertListEqual(
            _get_translation_language_choices(),
            [
                (None, '---------'),
                ('en', 'English'),
                ('de', 'German'),
                ('tr', 'Turkish')
            ]
        )

    @override_settings(LANGUAGE_CODE='xx')
    def test_invalid_default_language_code(self):
        with self.assertRaises(ValueError) as error:
            _get_translation_language_choices()

        self.assertEqual(
            error.exception.args[0],
            'The language code `xx` is not supported.'
        )
