from django.test import TestCase
from django.core.exceptions import FieldDoesNotExist
from django.utils.translation import activate

from translations.utils import get_validated_language, \
    get_validated_context_info, get_related_query_name

from places.models import Continent, Country, City


class GetValidatedLanguageTest(TestCase):

    def test_get_validated_language_with_active_lang(self):
        """Make sure it works with an active language."""
        activate('en')
        self.assertEqual(
            get_validated_language(),
            'en'
        )

    def test_get_validated_language_with_new_active_lang(self):
        """Make sure it works with a new active language."""
        activate('de')
        self.assertEqual(
            get_validated_language(),
            'de'
        )

    def test_get_validated_language_with_valid_lang(self):
        """Make sure it works with a valid language code."""
        self.assertEqual(
            get_validated_language('de'),
            'de'
        )

    def test_get_validated_language_with_invalid_lang(self):
        """Make sure it raises on an invalid language code."""
        with self.assertRaises(ValueError) as error:
            get_validated_language('xx')
        self.assertEqual(
            error.exception.args[0],
            "The language code `xx` is not supported."
        )


class GetValidatedContextInfoTest(TestCase):

    def test_get_validated_context_info_with_model_instance(self):
        """Make sure it works with a model instance."""
        eu = Continent.objects.create(name="Europe", code="EU")
        self.assertEqual(
            get_validated_context_info(eu),
            (Continent, False)
        )

    def test_get_validated_context_info_with_model_queryset(self):
        """Make sure it works with a model queryset."""
        Continent.objects.create(name="Europe", code="EU")
        Continent.objects.create(name="Asia", code="AS")
        continents = Continent.objects.all()
        self.assertEqual(
            get_validated_context_info(continents),
            (Continent, True)
        )

    def test_get_validated_context_info_with_model_iterable(self):
        """Make sure it works with a model iterable."""
        continents = []
        continents.append(Continent.objects.create(name="Europe", code="EU"))
        continents.append(Continent.objects.create(name="Asia", code="AS"))
        self.assertEqual(
            get_validated_context_info(continents),
            (Continent, True)
        )

    def test_get_validated_context_info_with_empty_list(self):
        """Make sure it works with an empty list."""
        self.assertEqual(
            get_validated_context_info([]),
            (None, True)
        )

    def test_get_validated_context_info_with_empty_queryset(self):
        """Make sure it works with an empty queryset."""
        self.assertEqual(
            get_validated_context_info(Continent.objects.none()),
            (None, True)
        )

    def test_get_validated_context_info_with_simple_instance(self):
        """Make sure it raises on simple instance."""
        class Person:
            def __init__(self, name):
                self.name = name

            def __str__(self):
                return self.name

            def __repr__(self):
                return self.name

        behzad = Person('Behzad')
        with self.assertRaises(TypeError) as error:
            get_validated_context_info(behzad)
        self.assertEqual(
            error.exception.args[0],
            "`Behzad` is neither a model instance nor an iterable of model instances."
        )

    def test_get_validated_context_info_with_simple_iterable(self):
        """Make sure it raises on simple iterable."""
        class Person:
            def __init__(self, name):
                self.name = name

            def __str__(self):
                return self.name

            def __repr__(self):
                return self.name

        people = []
        people.append(Person('Behzad'))
        people.append(Person('Max'))
        with self.assertRaises(TypeError) as error:
            get_validated_context_info(people)
        self.assertEqual(
            error.exception.args[0],
            "`[Behzad, Max]` is neither a model instance nor an iterable of model instances."
        )


class GetRelatedQueryNameTest(TestCase):

    def test_get_related_query_name_with_valid_relation(self):
        """Make sure it works with a valid relation."""
        self.assertEqual(
            get_related_query_name(Continent, 'countries__cities'),
            'country__continent'
        )

    def test_get_related_query_name_with_reverse_valid_relation(self):
        """Make sure it works with a valid relation in reverse."""
        self.assertEqual(
            get_related_query_name(City, 'country__continent'),
            'countries__cities'
        )

    def test_get_related_query_name_with_translations(self):
        """Make sure it works with translations relation."""
        self.assertEqual(
            get_related_query_name(Continent, 'countries__cities__translations'),
            'places_city__country__continent'
        )

    def test_get_related_query_name_with_reverse_translations(self):
        """Make sure it works with translations relation in reverse."""
        self.assertEqual(
            get_related_query_name(City, 'country__continent__translations'),
            'places_continent__countries__cities'
        )

    def test_get_related_query_name_with_empty_relation(self):
        """Make sure it raises on an empty relation."""
        with self.assertRaises(FieldDoesNotExist) as error:
            get_related_query_name(
                Continent,
                ''
            )
        self.assertEqual(
            error.exception.args[0],
            "Continent has no field named ''"
        )

    def test_get_related_query_name_with_invalid_relation(self):
        """Make sure it raises on an invalid relation."""
        with self.assertRaises(FieldDoesNotExist) as error:
            get_related_query_name(
                Continent,
                'wrong'
            )
        self.assertEqual(
            error.exception.args[0],
            "Continent has no field named 'wrong'"
        )

    def test_get_related_query_name_with_invalid_nested_relation(self):
        """Make sure it raises on an invalid nested relation."""
        with self.assertRaises(FieldDoesNotExist) as error:
            get_related_query_name(
                Continent,
                'countries__wrong'
            )
        self.assertEqual(
            error.exception.args[0],
            "Country has no field named 'wrong'"
        )
