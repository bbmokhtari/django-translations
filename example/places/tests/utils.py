from django.test import TestCase
from django.db import models
from django.core.exceptions import FieldDoesNotExist
from django.utils.translation import activate, deactivate

from translations.utils import get_validated_language, \
    get_validated_context_info, get_reverse_relation, \
    get_translations_reverse_relation, get_translations

from places.models import Continent, Country, City

from .samples import create_continent, create_country, create_city


class GetValidatedLanguageTest(TestCase):
    """Tests for `get_validated_language`."""

    def test_active_lang(self):
        """Make sure it works with an active language."""
        activate('en')
        self.assertEqual(
            get_validated_language(),
            'en'
        )

    def test_new_active_lang(self):
        """Make sure it works with a new active language."""
        activate('de')
        self.assertEqual(
            get_validated_language(),
            'de'
        )

    def test_valid_lang(self):
        """Make sure it works with a valid language code."""
        self.assertEqual(
            get_validated_language('de'),
            'de'
        )

    def test_invalid_lang(self):
        """Make sure it raises on an invalid language code."""
        with self.assertRaises(ValueError) as error:
            get_validated_language('xx')
        self.assertEqual(
            error.exception.args[0],
            "The language code `xx` is not supported."
        )


class GetValidatedContextInfoTest(TestCase):
    """Tests for `get_validated_context_info`."""

    def test_model_instance(self):
        """Make sure it works with a model instance."""
        europe = create_continent("europe")
        self.assertEqual(
            get_validated_context_info(europe),
            (Continent, False)
        )

    def test_model_queryset(self):
        """Make sure it works with a model queryset."""
        create_continent("europe")
        create_continent("asia")
        continents = Continent.objects.all()
        self.assertEqual(
            get_validated_context_info(continents),
            (Continent, True)
        )

    def test_model_iterable(self):
        """Make sure it works with a model iterable."""
        continents = []
        continents.append(create_continent("europe"))
        continents.append(create_continent("asia"))
        self.assertEqual(
            get_validated_context_info(continents),
            (Continent, True)
        )

    def test_empty_list(self):
        """Make sure it works with an empty list."""
        self.assertEqual(
            get_validated_context_info([]),
            (None, True)
        )

    def test_empty_queryset(self):
        """Make sure it works with an empty queryset."""
        continents = Continent.objects.none()
        self.assertEqual(
            get_validated_context_info(continents),
            (None, True)
        )

    def test_invalid_instance(self):
        """Make sure it raises on invalid instance."""
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

    def test_invalid_iterable(self):
        """Make sure it raises on invalid iterable."""
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


class GetReverseRelationTest(TestCase):
    """Tests for `get_reverse_relation`."""

    def test_simple_relation(self):
        """Make sure it works with a simple relation."""
        self.assertEqual(
            get_reverse_relation(Continent, 'countries'),
            'continent'
        )

    def test_simple_reverse_relation(self):
        """Make sure it works with a simple relation in reverse."""
        self.assertEqual(
            get_reverse_relation(Country, 'continent'),
            'countries'
        )

    def test_nested_relation(self):
        """Make sure it works with a nested relation."""
        self.assertEqual(
            get_reverse_relation(Continent, 'countries__cities'),
            'country__continent'
        )

    def test_nested_reverse_relation(self):
        """Make sure it works with a nested relation in reverse."""
        self.assertEqual(
            get_reverse_relation(City, 'country__continent'),
            'countries__cities'
        )

    def test_empty_relation(self):
        """Make sure it raises on an empty relation."""
        with self.assertRaises(FieldDoesNotExist) as error:
            get_reverse_relation(
                Continent,
                ''
            )
        self.assertEqual(
            error.exception.args[0],
            "Continent has no field named ''"
        )

    def test_invalid_simple_relation(self):
        """Make sure it raises on an invalid simple relation."""
        with self.assertRaises(FieldDoesNotExist) as error:
            get_reverse_relation(
                Continent,
                'wrong'
            )
        self.assertEqual(
            error.exception.args[0],
            "Continent has no field named 'wrong'"
        )

    def test_invalid_nested_relation(self):
        """Make sure it raises on an invalid nested relation."""
        with self.assertRaises(FieldDoesNotExist) as error:
            get_reverse_relation(
                Continent,
                'countries__wrong'
            )
        self.assertEqual(
            error.exception.args[0],
            "Country has no field named 'wrong'"
        )


class GetTranslationsReverseRelationTest(TestCase):
    """Tests for `get_translations_reverse_relation`."""

    def test_simple_relation(self):
        """Make sure it works with a simple relation."""
        self.assertEqual(
            get_translations_reverse_relation(Continent, 'countries'),
            'places_country__continent'
        )

    def test_simple_reverse_relation(self):
        """Make sure it works with a simple relation in reverse."""
        self.assertEqual(
            get_translations_reverse_relation(Country, 'continent'),
            'places_continent__countries'
        )

    def test_nested_relation(self):
        """Make sure it works with a nested relation."""
        self.assertEqual(
            get_translations_reverse_relation(Continent, 'countries__cities'),
            'places_city__country__continent'
        )

    def test_nested_reverse_relation(self):
        """Make sure it works with a nested relation in reverse."""
        self.assertEqual(
            get_translations_reverse_relation(City, 'country__continent'),
            'places_continent__countries__cities'
        )

    def test_none_relation(self):
        """Make sure it works with None relation."""
        self.assertEqual(
            get_translations_reverse_relation(Continent),
            'places_continent'
        )

    def test_empty_relation(self):
        """Make sure it raises on an empty relation."""
        with self.assertRaises(FieldDoesNotExist) as error:
            get_translations_reverse_relation(
                Continent,
                ''
            )
        self.assertEqual(
            error.exception.args[0],
            "Continent has no field named ''"
        )

    def test_invalid_simple_relation(self):
        """Make sure it raises on an invalid simple relation."""
        with self.assertRaises(FieldDoesNotExist) as error:
            get_translations_reverse_relation(
                Continent,
                'wrong'
            )
        self.assertEqual(
            error.exception.args[0],
            "Continent has no field named 'wrong'"
        )

    def test_invalid_nested_relation(self):
        """Make sure it raises on an invalid nested relation."""
        with self.assertRaises(FieldDoesNotExist) as error:
            get_translations_reverse_relation(
                Continent,
                'countries__wrong'
            )
        self.assertEqual(
            error.exception.args[0],
            "Country has no field named 'wrong'"
        )


class GetTranslationsTest(TestCase):
    """Tests for `get_translations`."""

    # ---- arguments testing -------------------------------------------------

    def test_instance_with_no_relation_and_with_no_lang(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de"],
        )

        activate("de")
        self.assertQuerysetEqual(
            get_translations(
                europe
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
            ]
        )

    def test_instance_with_simple_relation_and_with_no_lang(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de"]
        )

        activate("de")
        self.assertQuerysetEqual(
            get_translations(
                europe,
                "countries"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
            ]
        )

    def test_instance_with_nested_relation_and_with_no_lang(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de"]
        )
        germany = create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_city(
            germany,
            "cologne",
            fields=["name", "denonym"],
            langs=["de"]
        )

        activate("de")
        self.assertQuerysetEqual(
            get_translations(
                europe,
                "countries", "countries__cities"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
                "<Translation: Cologne: Köln>",
                "<Translation: Cologner: Kölner>",
            ]
        )

    def test_instance_with_no_relation_and_with_lang(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de"],
        )

        self.assertQuerysetEqual(
            get_translations(
                europe,
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
            ]
        )

    def test_instance_with_simple_relation_and_with_lang(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de"]
        )

        self.assertQuerysetEqual(
            get_translations(
                europe,
                "countries",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
            ]
        )

    def test_instance_with_nested_relation_and_with_lang(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de"]
        )
        germany = create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_city(
            germany,
            "cologne",
            fields=["name", "denonym"],
            langs=["de"]
        )

        self.assertQuerysetEqual(
            get_translations(
                europe,
                "countries", "countries__cities",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
                "<Translation: Cologne: Köln>",
                "<Translation: Cologner: Kölner>",
            ]
        )

    def test_queryset_with_no_relation_and_with_no_lang(self):
        create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de"],
        )

        create_continent(
            "asia",
            fields=["name", "denonym"],
            langs=["de"],
        )

        continents = Continent.objects.all()

        activate("de")
        self.assertQuerysetEqual(
            get_translations(
                continents
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
            ]
        )

    def test_queryset_with_simple_relation_and_with_no_lang(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de"]
        )

        asia = create_continent(
            "asia",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_country(
            asia,
            "india",
            fields=["name", "denonym"],
            langs=["de"]
        )

        continents = Continent.objects.all()

        activate("de")
        self.assertQuerysetEqual(
            get_translations(
                continents,
                "countries"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: India: Indien>",
                "<Translation: Indian: Indisch>",
            ]
        )

    def test_queryset_with_nested_relation_and_with_no_lang(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de"]
        )
        germany = create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_city(
            germany,
            "cologne",
            fields=["name", "denonym"],
            langs=["de"]
        )

        asia = create_continent(
            "asia",
            fields=["name", "denonym"],
            langs=["de"]
        )
        india = create_country(
            asia,
            "india",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_city(
            india,
            "mumbai",
            fields=["name", "denonym"],
            langs=["de"]
        )

        continents = Continent.objects.all()

        activate("de")
        self.assertQuerysetEqual(
            get_translations(
                continents,
                "countries", "countries__cities"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
                "<Translation: Cologne: Köln>",
                "<Translation: Cologner: Kölner>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: India: Indien>",
                "<Translation: Indian: Indisch>",
                "<Translation: Mumbai: Mumbaï>",
                "<Translation: Mumbaian: Mumbäisch>",
            ]
        )

    def test_queryset_with_no_relation_and_with_lang(self):
        create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de"],
        )

        create_continent(
            "asia",
            fields=["name", "denonym"],
            langs=["de"],
        )

        continents = Continent.objects.all()

        self.assertQuerysetEqual(
            get_translations(
                continents,
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
            ]
        )

    def test_queryset_with_simple_relation_and_with_lang(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de"]
        )

        asia = create_continent(
            "asia",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_country(
            asia,
            "india",
            fields=["name", "denonym"],
            langs=["de"]
        )

        continents = Continent.objects.all()

        self.assertQuerysetEqual(
            get_translations(
                continents,
                "countries",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: India: Indien>",
                "<Translation: Indian: Indisch>",
            ]
        )

    def test_queryset_with_nested_relation_and_with_lang(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de"]
        )
        germany = create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_city(
            germany,
            "cologne",
            fields=["name", "denonym"],
            langs=["de"]
        )

        asia = create_continent(
            "asia",
            fields=["name", "denonym"],
            langs=["de"]
        )
        india = create_country(
            asia,
            "india",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_city(
            india,
            "mumbai",
            fields=["name", "denonym"],
            langs=["de"]
        )

        continents = Continent.objects.all()

        self.assertQuerysetEqual(
            get_translations(
                continents,
                "countries", "countries__cities",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
                "<Translation: Cologne: Köln>",
                "<Translation: Cologner: Kölner>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: India: Indien>",
                "<Translation: Indian: Indisch>",
                "<Translation: Mumbai: Mumbaï>",
                "<Translation: Mumbaian: Mumbäisch>",
            ]
        )

    # ---- specific filtering testing ----------------------------------------

    def test_instance_with_no_relation_lang_filtering(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de", "tr"],
        )

        self.assertQuerysetEqual(
            get_translations(
                europe,
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                europe,
                lang="tr"
            ).order_by("id"),
            [
                "<Translation: Europe: Avrupa>",
                "<Translation: European: Avrupalı>",
            ]
        )

    def test_instance_with_simple_relation_lang_filtering(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        self.assertQuerysetEqual(
            get_translations(
                europe,
                "countries",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                europe,
                "countries",
                lang="tr"
            ).order_by("id"),
            [
                "<Translation: Europe: Avrupa>",
                "<Translation: European: Avrupalı>",
                "<Translation: Germany: Almanya>",
                "<Translation: German: Almanca>",
            ]
        )

    def test_instance_with_nested_relation_lang_filtering(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        germany = create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            germany,
            "cologne",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        self.assertQuerysetEqual(
            get_translations(
                europe,
                "countries", "countries__cities",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
                "<Translation: Cologne: Köln>",
                "<Translation: Cologner: Kölner>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                europe,
                "countries", "countries__cities",
                lang="tr"
            ).order_by("id"),
            [
                "<Translation: Europe: Avrupa>",
                "<Translation: European: Avrupalı>",
                "<Translation: Germany: Almanya>",
                "<Translation: German: Almanca>",
                "<Translation: Cologne: Koln>",
                "<Translation: Cologner: Kolnlı>",
            ]
        )

    def test_instance_with_no_relation_relation_filtering(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de"],
        )
        germany = create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_city(
            germany,
            "cologne",
            fields=["name", "denonym"],
            langs=["de"]
        )

        self.assertQuerysetEqual(
            get_translations(
                europe,
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
            ]
        )

    def test_instance_with_simple_relation_relation_filtering(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de"]
        )
        germany = create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_city(
            germany,
            "cologne",
            fields=["name", "denonym"],
            langs=["de"]
        )

        self.assertQuerysetEqual(
            get_translations(
                europe,
                "countries",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
            ]
        )

    def test_instance_with_nested_relation_relation_filtering(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de"]
        )
        germany = create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_city(
            germany,
            "cologne",
            fields=["name", "denonym"],
            langs=["de"]
        )

        self.assertQuerysetEqual(
            get_translations(
                europe,
                "countries", "countries__cities",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
                "<Translation: Cologne: Köln>",
                "<Translation: Cologner: Kölner>",
            ]
        )

    def test_instance_with_no_relation_context_filtering(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de"],
        )
        asia = create_continent(
            "asia",
            fields=["name", "denonym"],
            langs=["de"]
        )

        self.assertQuerysetEqual(
            get_translations(
                europe,
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                asia,
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
            ]
        )

    def test_instance_with_simple_relation_context_filtering(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de"]
        )

        asia = create_continent(
            "asia",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_country(
            asia,
            "india",
            fields=["name", "denonym"],
            langs=["de"]
        )

        self.assertQuerysetEqual(
            get_translations(
                europe,
                "countries",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                asia,
                "countries",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: India: Indien>",
                "<Translation: Indian: Indisch>",
            ]
        )

    def test_instance_with_nested_relation_context_filtering(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de"]
        )
        germany = create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_city(
            germany,
            "cologne",
            fields=["name", "denonym"],
            langs=["de"]
        )

        asia = create_continent(
            "asia",
            fields=["name", "denonym"],
            langs=["de"]
        )
        india = create_country(
            asia,
            "india",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_city(
            india,
            "mumbai",
            fields=["name", "denonym"],
            langs=["de"]
        )

        self.assertQuerysetEqual(
            get_translations(
                europe,
                "countries", "countries__cities",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
                "<Translation: Cologne: Köln>",
                "<Translation: Cologner: Kölner>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                asia,
                "countries", "countries__cities",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: India: Indien>",
                "<Translation: Indian: Indisch>",
                "<Translation: Mumbai: Mumbaï>",
                "<Translation: Mumbaian: Mumbäisch>",
            ]
        )

    def test_queryset_with_no_relation_lang_filtering(self):
        create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de", "tr"],
        )

        create_continent(
            "asia",
            fields=["name", "denonym"],
            langs=["de", "tr"],
        )

        continents = Continent.objects.all()

        self.assertQuerysetEqual(
            get_translations(
                continents,
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                continents,
                lang="tr"
            ).order_by("id"),
            [
                "<Translation: Europe: Avrupa>",
                "<Translation: European: Avrupalı>",
                "<Translation: Asia: Asya>",
                "<Translation: Asian: Asyalı>",
            ]
        )

    def test_queryset_with_simple_relation_lang_filtering(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        asia = create_continent(
            "asia",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_country(
            asia,
            "india",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        continents = Continent.objects.all()

        self.assertQuerysetEqual(
            get_translations(
                continents,
                "countries",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: India: Indien>",
                "<Translation: Indian: Indisch>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                continents,
                "countries",
                lang="tr"
            ).order_by("id"),
            [
                "<Translation: Europe: Avrupa>",
                "<Translation: European: Avrupalı>",
                "<Translation: Germany: Almanya>",
                "<Translation: German: Almanca>",
                "<Translation: Asia: Asya>",
                "<Translation: Asian: Asyalı>",
                "<Translation: India: Hindistan>",
                "<Translation: Indian: Hintlı>",
            ]
        )

    def test_queryset_with_nested_relation_lang_filtering(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        germany = create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            germany,
            "cologne",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        asia = create_continent(
            "asia",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        india = create_country(
            asia,
            "india",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            india,
            "mumbai",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        continents = Continent.objects.all()

        self.assertQuerysetEqual(
            get_translations(
                continents,
                "countries", "countries__cities",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
                "<Translation: Cologne: Köln>",
                "<Translation: Cologner: Kölner>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: India: Indien>",
                "<Translation: Indian: Indisch>",
                "<Translation: Mumbai: Mumbaï>",
                "<Translation: Mumbaian: Mumbäisch>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                continents,
                "countries", "countries__cities",
                lang="tr"
            ).order_by("id"),
            [
                "<Translation: Europe: Avrupa>",
                "<Translation: European: Avrupalı>",
                "<Translation: Germany: Almanya>",
                "<Translation: German: Almanca>",
                "<Translation: Cologne: Koln>",
                "<Translation: Cologner: Kolnlı>",
                "<Translation: Asia: Asya>",
                "<Translation: Asian: Asyalı>",
                "<Translation: India: Hindistan>",
                "<Translation: Indian: Hintlı>",
                "<Translation: Mumbai: Bombay>",
                "<Translation: Mumbaian: Bombaylı>",
            ]
        )

    def test_queryset_with_no_relation_relation_filtering(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        germany = create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            germany,
            "cologne",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        asia = create_continent(
            "asia",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        india = create_country(
            asia,
            "india",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            india,
            "mumbai",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        continents = Continent.objects.all()

        self.assertQuerysetEqual(
            get_translations(
                continents,
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
            ]
        )

    def test_queryset_with_simple_relation_relation_filtering(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        germany = create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            germany,
            "cologne",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        asia = create_continent(
            "asia",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        india = create_country(
            asia,
            "india",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            india,
            "mumbai",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        continents = Continent.objects.all()

        self.assertQuerysetEqual(
            get_translations(
                continents,
                "countries",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: India: Indien>",
                "<Translation: Indian: Indisch>",
            ]
        )

    def test_queryset_with_nested_relation_relation_filtering(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        germany = create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            germany,
            "cologne",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        asia = create_continent(
            "asia",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        india = create_country(
            asia,
            "india",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            india,
            "mumbai",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        continents = Continent.objects.all()

        self.assertQuerysetEqual(
            get_translations(
                continents,
                "countries", "countries__cities",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
                "<Translation: Cologne: Köln>",
                "<Translation: Cologner: Kölner>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: India: Indien>",
                "<Translation: Indian: Indisch>",
                "<Translation: Mumbai: Mumbaï>",
                "<Translation: Mumbaian: Mumbäisch>",
            ]
        )

    def test_queryset_with_no_relation_context_filtering(self):
        create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de"],
        )
        create_continent(
            "asia",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_continent(
            "africa",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_continent(
            "north america",
            fields=["name", "denonym"],
            langs=["de"]
        )

        eurasia = Continent.objects.filter(
            models.Q(name="Asia") | models.Q(name="Europe")
        )
        afromerica = Continent.objects.filter(
            models.Q(name="Africa") | models.Q(name="North America")
        )

        self.assertQuerysetEqual(
            get_translations(
                eurasia,
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                afromerica,
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Africa: Afrika>",
                "<Translation: African: Afrikanisch>",
                "<Translation: North America: Nordamerika>",
                "<Translation: North American: Nordamerikanisch>",
            ]
        )

    def test_queryset_with_simple_relation_context_filtering(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de"]
        )

        asia = create_continent(
            "asia",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_country(
            asia,
            "india",
            fields=["name", "denonym"],
            langs=["de"]
        )

        africa = create_continent(
            "africa",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_country(
            africa,
            "egypt",
            fields=["name", "denonym"],
            langs=["de"]
        )

        north_america = create_continent(
            "north america",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_country(
            north_america,
            "mexico",
            fields=["name", "denonym"],
            langs=["de"]
        )

        eurasia = Continent.objects.filter(
            models.Q(name="Asia") | models.Q(name="Europe")
        )
        afromerica = Continent.objects.filter(
            models.Q(name="Africa") | models.Q(name="North America")
        )

        self.assertQuerysetEqual(
            get_translations(
                eurasia,
                "countries",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: India: Indien>",
                "<Translation: Indian: Indisch>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                afromerica,
                "countries",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Africa: Afrika>",
                "<Translation: African: Afrikanisch>",
                "<Translation: Egypt: Ägypten>",
                "<Translation: Egyptian: Ägyptisch>",
                "<Translation: North America: Nordamerika>",
                "<Translation: North American: Nordamerikanisch>",
                "<Translation: Mexico: Mexiko>",
                "<Translation: Mexican: Mexikaner>",
            ]
        )

    def test_queryset_with_nested_relation_context_filtering(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de"]
        )
        germany = create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_city(
            germany,
            "cologne",
            fields=["name", "denonym"],
            langs=["de"]
        )

        asia = create_continent(
            "asia",
            fields=["name", "denonym"],
            langs=["de"]
        )
        india = create_country(
            asia,
            "india",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_city(
            india,
            "mumbai",
            fields=["name", "denonym"],
            langs=["de"]
        )

        africa = create_continent(
            "africa",
            fields=["name", "denonym"],
            langs=["de"]
        )
        egypt = create_country(
            africa,
            "egypt",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_city(
            egypt,
            "cairo",
            fields=["name", "denonym"],
            langs=["de"]
        )

        north_america = create_continent(
            "north america",
            fields=["name", "denonym"],
            langs=["de"]
        )
        mexico = create_country(
            north_america,
            "mexico",
            fields=["name", "denonym"],
            langs=["de"]
        )
        create_city(
            mexico,
            "mexico city",
            fields=["name", "denonym"],
            langs=["de"]
        )

        eurasia = Continent.objects.filter(
            models.Q(name="Asia") | models.Q(name="Europe")
        )
        afromerica = Continent.objects.filter(
            models.Q(name="Africa") | models.Q(name="North America")
        )

        self.assertQuerysetEqual(
            get_translations(
                eurasia,
                "countries", "countries__cities",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
                "<Translation: Cologne: Köln>",
                "<Translation: Cologner: Kölner>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: India: Indien>",
                "<Translation: Indian: Indisch>",
                "<Translation: Mumbai: Mumbaï>",
                "<Translation: Mumbaian: Mumbäisch>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                afromerica,
                "countries", "countries__cities",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Africa: Afrika>",
                "<Translation: African: Afrikanisch>",
                "<Translation: Egypt: Ägypten>",
                "<Translation: Egyptian: Ägyptisch>",
                "<Translation: Cairo: Kairo>",
                "<Translation: Cairoian: Kairoisch>",
                "<Translation: North America: Nordamerika>",
                "<Translation: North American: Nordamerikanisch>",
                "<Translation: Mexico: Mexiko>",
                "<Translation: Mexican: Mexikaner>",
                "<Translation: Mexico City: Mexiko Stadt>",
                "<Translation: Mexico Citian: Mexiko Stadtisch>",
            ]
        )

    # ---- global filtering testing ------------------------------------------

    def test_instance_with_no_relation_filtering(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        germany = create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            germany,
            "cologne",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        asia = create_continent(
            "asia",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        india = create_country(
            asia,
            "india",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            india,
            "mumbai",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        self.assertQuerysetEqual(
            get_translations(
                europe,
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                europe,
                lang="tr"
            ).order_by("id"),
            [
                "<Translation: Europe: Avrupa>",
                "<Translation: European: Avrupalı>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                asia,
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                asia,
                lang="tr"
            ).order_by("id"),
            [
                "<Translation: Asia: Asya>",
                "<Translation: Asian: Asyalı>",
            ]
        )

    def test_instance_with_simple_relation_filtering(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        germany = create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            germany,
            "cologne",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        asia = create_continent(
            "asia",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        india = create_country(
            asia,
            "india",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            india,
            "mumbai",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        self.assertQuerysetEqual(
            get_translations(
                europe,
                "countries",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                europe,
                "countries",
                lang="tr"
            ).order_by("id"),
            [
                "<Translation: Europe: Avrupa>",
                "<Translation: European: Avrupalı>",
                "<Translation: Germany: Almanya>",
                "<Translation: German: Almanca>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                asia,
                "countries",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: India: Indien>",
                "<Translation: Indian: Indisch>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                asia,
                "countries",
                lang="tr"
            ).order_by("id"),
            [
                "<Translation: Asia: Asya>",
                "<Translation: Asian: Asyalı>",
                "<Translation: India: Hindistan>",
                "<Translation: Indian: Hintlı>",
            ]
        )

    def test_instance_with_nested_relation_filtering(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        germany = create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            germany,
            "cologne",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        asia = create_continent(
            "asia",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        india = create_country(
            asia,
            "india",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            india,
            "mumbai",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        self.assertQuerysetEqual(
            get_translations(
                europe,
                "countries", "countries__cities",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
                "<Translation: Cologne: Köln>",
                "<Translation: Cologner: Kölner>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                europe,
                "countries", "countries__cities",
                lang="tr"
            ).order_by("id"),
            [
                "<Translation: Europe: Avrupa>",
                "<Translation: European: Avrupalı>",
                "<Translation: Germany: Almanya>",
                "<Translation: German: Almanca>",
                "<Translation: Cologne: Koln>",
                "<Translation: Cologner: Kolnlı>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                asia,
                "countries", "countries__cities",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: India: Indien>",
                "<Translation: Indian: Indisch>",
                "<Translation: Mumbai: Mumbaï>",
                "<Translation: Mumbaian: Mumbäisch>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                asia,
                "countries", "countries__cities",
                lang="tr"
            ).order_by("id"),
            [
                "<Translation: Asia: Asya>",
                "<Translation: Asian: Asyalı>",
                "<Translation: India: Hindistan>",
                "<Translation: Indian: Hintlı>",
                "<Translation: Mumbai: Bombay>",
                "<Translation: Mumbaian: Bombaylı>",
            ]
        )

    def test_queryset_with_no_relation_filtering(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        germany = create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            germany,
            "cologne",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        asia = create_continent(
            "asia",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        india = create_country(
            asia,
            "india",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            india,
            "mumbai",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        africa = create_continent(
            "africa",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        egypt = create_country(
            africa,
            "egypt",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            egypt,
            "cairo",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        north_america = create_continent(
            "north america",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        mexico = create_country(
            north_america,
            "mexico",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            mexico,
            "mexico city",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        eurasia = Continent.objects.filter(
            models.Q(name="Asia") | models.Q(name="Europe")
        )
        afromerica = Continent.objects.filter(
            models.Q(name="Africa") | models.Q(name="North America")
        )

        self.assertQuerysetEqual(
            get_translations(
                eurasia,
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                eurasia,
                lang="tr"
            ).order_by("id"),
            [
                "<Translation: Europe: Avrupa>",
                "<Translation: European: Avrupalı>",
                "<Translation: Asia: Asya>",
                "<Translation: Asian: Asyalı>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                afromerica,
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Africa: Afrika>",
                "<Translation: African: Afrikanisch>",
                "<Translation: North America: Nordamerika>",
                "<Translation: North American: Nordamerikanisch>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                afromerica,
                lang="tr"
            ).order_by("id"),
            [
                "<Translation: Africa: Àfrika>",
                "<Translation: African: Àfrikalı>",
                "<Translation: North America: Kuzey Amerika>",
                "<Translation: North American: Kuzey Amerikalı>",
            ]
        )

    def test_queryset_with_simple_relation_filtering(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        germany = create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            germany,
            "cologne",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        asia = create_continent(
            "asia",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        india = create_country(
            asia,
            "india",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            india,
            "mumbai",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        africa = create_continent(
            "africa",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        egypt = create_country(
            africa,
            "egypt",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            egypt,
            "cairo",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        north_america = create_continent(
            "north america",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        mexico = create_country(
            north_america,
            "mexico",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            mexico,
            "mexico city",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        eurasia = Continent.objects.filter(
            models.Q(name="Asia") | models.Q(name="Europe")
        )
        afromerica = Continent.objects.filter(
            models.Q(name="Africa") | models.Q(name="North America")
        )

        self.assertQuerysetEqual(
            get_translations(
                eurasia,
                "countries",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: India: Indien>",
                "<Translation: Indian: Indisch>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                eurasia,
                "countries",
                lang="tr"
            ).order_by("id"),
            [
                "<Translation: Europe: Avrupa>",
                "<Translation: European: Avrupalı>",
                "<Translation: Germany: Almanya>",
                "<Translation: German: Almanca>",
                "<Translation: Asia: Asya>",
                "<Translation: Asian: Asyalı>",
                "<Translation: India: Hindistan>",
                "<Translation: Indian: Hintlı>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                afromerica,
                "countries",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Africa: Afrika>",
                "<Translation: African: Afrikanisch>",
                "<Translation: Egypt: Ägypten>",
                "<Translation: Egyptian: Ägyptisch>",
                "<Translation: North America: Nordamerika>",
                "<Translation: North American: Nordamerikanisch>",
                "<Translation: Mexico: Mexiko>",
                "<Translation: Mexican: Mexikaner>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                afromerica,
                "countries",
                lang="tr"
            ).order_by("id"),
            [
                "<Translation: Africa: Àfrika>",
                "<Translation: African: Àfrikalı>",
                "<Translation: Egypt: Mısır>",
                "<Translation: Egyptian: Mısırlı>",
                "<Translation: North America: Kuzey Amerika>",
                "<Translation: North American: Kuzey Amerikalı>",
                "<Translation: Mexico: Meksika>",
                "<Translation: Mexican: Meksikalı>",
            ]
        )

    def test_queryset_with_nested_relation_filtering(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        germany = create_country(
            europe,
            "germany",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            germany,
            "cologne",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        asia = create_continent(
            "asia",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        india = create_country(
            asia,
            "india",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            india,
            "mumbai",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        africa = create_continent(
            "africa",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        egypt = create_country(
            africa,
            "egypt",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            egypt,
            "cairo",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        north_america = create_continent(
            "north america",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        mexico = create_country(
            north_america,
            "mexico",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        create_city(
            mexico,
            "mexico city",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        eurasia = Continent.objects.filter(
            models.Q(name="Asia") | models.Q(name="Europe")
        )
        afromerica = Continent.objects.filter(
            models.Q(name="Africa") | models.Q(name="North America")
        )

        self.assertQuerysetEqual(
            get_translations(
                eurasia,
                "countries", "countries__cities",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
                "<Translation: Cologne: Köln>",
                "<Translation: Cologner: Kölner>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: India: Indien>",
                "<Translation: Indian: Indisch>",
                "<Translation: Mumbai: Mumbaï>",
                "<Translation: Mumbaian: Mumbäisch>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                eurasia,
                "countries", "countries__cities",
                lang="tr"
            ).order_by("id"),
            [
                "<Translation: Europe: Avrupa>",
                "<Translation: European: Avrupalı>",
                "<Translation: Germany: Almanya>",
                "<Translation: German: Almanca>",
                "<Translation: Cologne: Koln>",
                "<Translation: Cologner: Kolnlı>",
                "<Translation: Asia: Asya>",
                "<Translation: Asian: Asyalı>",
                "<Translation: India: Hindistan>",
                "<Translation: Indian: Hintlı>",
                "<Translation: Mumbai: Bombay>",
                "<Translation: Mumbaian: Bombaylı>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                afromerica,
                "countries", "countries__cities",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Africa: Afrika>",
                "<Translation: African: Afrikanisch>",
                "<Translation: Egypt: Ägypten>",
                "<Translation: Egyptian: Ägyptisch>",
                "<Translation: Cairo: Kairo>",
                "<Translation: Cairoian: Kairoisch>",
                "<Translation: North America: Nordamerika>",
                "<Translation: North American: Nordamerikanisch>",
                "<Translation: Mexico: Mexiko>",
                "<Translation: Mexican: Mexikaner>",
                "<Translation: Mexico City: Mexiko Stadt>",
                "<Translation: Mexico Citian: Mexiko Stadtisch>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                afromerica,
                "countries", "countries__cities",
                lang="tr"
            ).order_by("id"),
            [
                "<Translation: Africa: Àfrika>",
                "<Translation: African: Àfrikalı>",
                "<Translation: Egypt: Mısır>",
                "<Translation: Egyptian: Mısırlı>",
                "<Translation: Cairo: Kahire>",
                "<Translation: Cairoian: Kahirelı>",
                "<Translation: North America: Kuzey Amerika>",
                "<Translation: North American: Kuzey Amerikalı>",
                "<Translation: Mexico: Meksika>",
                "<Translation: Mexican: Meksikalı>",
                "<Translation: Mexico City: Meksika şehri>",
                "<Translation: Mexico Citian: Meksika şehrilı>",
            ]
        )
