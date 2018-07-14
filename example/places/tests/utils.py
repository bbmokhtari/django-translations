from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils.translation import activate

from translations.utils import get_validated_language


class GetValidatedLanguageTest(TestCase):

    def test_get_validated_language(self):
        """Make sure default active language works."""
        activate('en')
        self.assertEqual(
            get_validated_language(),
            'en'
        )

    def test_get_validated_language_with_new_active_language(self):
        """Make sure a new active language works."""
        activate('de')
        self.assertEqual(
            get_validated_language(),
            'de'
        )

    def test_get_validated_language_with_given_language(self):
        """Make sure it works with argument passed."""
        self.assertEqual(
            get_validated_language('de'),
            'de'
        )

    def test_get_validated_language_raises_validation_error(self):
        """Make sure it raises `ValidationError` on invalid argument."""
        with self.assertRaises(ValidationError) as error:
            get_validated_language('xx')
        self.assertEqual(
            error.exception.args[0],
            "The language code `xx` is not supported."
        )
