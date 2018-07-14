from django.test import TestCase
from django.core.exceptions import ValidationError, FieldDoesNotExist
from django.utils.translation import activate

from translations.utils import get_validated_language, get_related_query_name

from places.models import Continent, Country, City


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


class GetRelatedQueryNameTest(TestCase):

    def test_get_related_query_name(self):
        """Make sure the function works properly."""
        self.assertEqual(
            get_related_query_name(Continent, 'countries__cities'),
            'country__continent'
        )

    def test_get_related_query_name_with_reverse(self):
        """Make sure the other way around works as well."""
        self.assertEqual(
            get_related_query_name(City, 'country__continent'),
            'countries__cities'
        )

    def test_get_related_query_name_with_translations(self):
        """Make sure translation works."""
        self.assertEqual(
            get_related_query_name(Continent, 'countries__cities__translations'),
            'places_city__country__continent'
        )

    def test_get_related_query_name_with_reverse_translations(self):
        """Make sure translation works the other way around."""
        self.assertEqual(
            get_related_query_name(City, 'country__continent__translations'),
            'places_continent__countries__cities'
        )

    def test_get_related_query_name_raises_field_does_not_exist_empty(self):
        """Make sure field error is raised on empty field name."""
        with self.assertRaises(FieldDoesNotExist) as error:
            get_related_query_name(
                Continent,
                ''
            )
        self.assertEqual(
            error.exception.args[0],
            "Continent has no field named ''"
        )

    def test_get_related_query_name_raises_field_does_not_exist_wrong(self):
        """Make sure field error is raised on wrong field name."""
        with self.assertRaises(FieldDoesNotExist) as error:
            get_related_query_name(
                Continent,
                'wrong'
            )
        self.assertEqual(
            error.exception.args[0],
            "Continent has no field named 'wrong'"
        )

    def test_get_related_query_name_raises_field_does_not_exist_nested(self):
        """Make sure field error is raised on wrong nested field."""
        with self.assertRaises(FieldDoesNotExist) as error:
            get_related_query_name(
                Continent,
                'countries__wrong'
            )
        self.assertEqual(
            error.exception.args[0],
            "Country has no field named 'wrong'"
        )
