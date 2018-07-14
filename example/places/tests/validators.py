from django.test import TestCase
from django.core.exceptions import ValidationError

from translations.validators import validate_language


class ValidateLanguageTest(TestCase):

    def test_validate_language(self):
        self.assertIs(validate_language('en'), None)

    def test_validate_language_invalid(self):
        with self.assertRaises(ValidationError) as error:
            validate_language('xx')
        self.assertEqual(
            error.exception.args[0],
            "The language code `xx` is not supported."
        )
