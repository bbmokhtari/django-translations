from django.test import TestCase
from django.core.exceptions import ValidationError

from translations.validators import validate_language, validate_context

from places.models import Continent


class ValidateLanguageTest(TestCase):

    def test_validate_language_with_valid_lang(self):
        """Make sure it works with a valid language code."""
        self.assertIs(validate_language('en'), None)

    def test_validate_language_with_invalid_lang(self):
        """Make sure it raises on an invalid language code."""
        with self.assertRaises(ValidationError) as error:
            validate_language('xx')
        self.assertEqual(
            error.exception.args[0],
            "The language code `xx` is not supported."
        )


class ValidateContextTest(TestCase):

    def test_validate_context_with_model_instance(self):
        """Make sure it works with a model instance."""
        eu = Continent.objects.create(name="Europe", code="EU")
        self.assertIs(validate_context(eu), None)

    def test_validate_context_with_model_queryset(self):
        """Make sure it works with a model queryset."""
        Continent.objects.create(name="Europe", code="EU")
        Continent.objects.create(name="Asia", code="AS")
        continents = Continent.objects.all()
        self.assertIs(validate_context(continents), None)

    def test_validate_context_with_model_iterable(self):
        """Make sure it works with a model iterable."""
        continents = []
        continents.append(Continent.objects.create(name="Europe", code="EU"))
        continents.append(Continent.objects.create(name="Asia", code="AS"))
        self.assertIs(validate_context(continents), None)

    def test_validate_context_with_empty_list(self):
        """Make sure it works with an empty list."""
        self.assertIs(validate_context([]), None)

    def test_validate_context_with_empty_queryset(self):
        """Make sure it works with an empty queryset."""
        self.assertIs(validate_context(Continent.objects.none()), None)

    def test_validate_context_with_simple_instance(self):
        """Make sure it raises on simple instance."""
        class Person:
            def __init__(self, name):
                self.name = name

            def __str__(self):
                return self.name

            def __repr__(self):
                return self.name

        behzad = Person('Behzad')
        with self.assertRaises(ValidationError) as error:
            validate_context(behzad)
        self.assertEqual(
            error.exception.args[0],
            "`Behzad` is neither a model instance nor an iterable of model instances."
        )

    def test_validate_context_with_simple_iterable(self):
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
        with self.assertRaises(ValidationError) as error:
            validate_context(people)
        self.assertEqual(
            error.exception.args[0],
            "`[Behzad, Max]` is neither a model instance nor an iterable of model instances."
        )
