from django.test import TestCase
from django.db import models
from django.core.exceptions import FieldDoesNotExist
from django.utils.translation import activate, deactivate
from django.contrib.contenttypes.models import ContentType

from translations.utils import get_translation_language, \
    get_context_details, get_reverse_relation, \
    get_translations_reverse_relation, get_translations, \
    get_dictionary, get_relations_details

from translations.models import Translation

from sample.models import Continent, Country, City

from .samples import create_continent, create_country, create_city


class GetValidatedLanguageTest(TestCase):
    """Tests for `get_translation_language`."""

    def test_active_lang(self):
        """Make sure it works with an active language."""
        activate('en')
        self.assertEqual(
            get_translation_language(),
            'en'
        )

    def test_new_active_lang(self):
        """Make sure it works with a new active language."""
        activate('de')
        self.assertEqual(
            get_translation_language(),
            'de'
        )

    def test_valid_lang(self):
        """Make sure it works with a valid language code."""
        self.assertEqual(
            get_translation_language('de'),
            'de'
        )

    def test_invalid_lang(self):
        """Make sure it raises on an invalid language code."""
        with self.assertRaises(ValueError) as error:
            get_translation_language('xx')
        self.assertEqual(
            error.exception.args[0],
            "The language code `xx` is not supported."
        )


class GetValidatedContextInfoTest(TestCase):
    """Tests for `get_context_details`."""

    def test_model_instance(self):
        """Make sure it works with a model instance."""
        europe = create_continent("europe")
        self.assertEqual(
            get_context_details(europe),
            (Continent, False)
        )

    def test_model_queryset(self):
        """Make sure it works with a model queryset."""
        create_continent("europe")
        create_continent("asia")
        continents = Continent.objects.all()
        self.assertEqual(
            get_context_details(continents),
            (Continent, True)
        )

    def test_model_iterable(self):
        """Make sure it works with a model iterable."""
        continents = []
        continents.append(create_continent("europe"))
        continents.append(create_continent("asia"))
        self.assertEqual(
            get_context_details(continents),
            (Continent, True)
        )

    def test_empty_list(self):
        """Make sure it works with an empty list."""
        self.assertEqual(
            get_context_details([]),
            (None, True)
        )

    def test_empty_queryset(self):
        """Make sure it works with an empty queryset."""
        continents = Continent.objects.none()
        self.assertEqual(
            get_context_details(continents),
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
            get_context_details(behzad)
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
            get_context_details(people)
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
            'sample_country__continent'
        )

    def test_simple_reverse_relation(self):
        """Make sure it works with a simple relation in reverse."""
        self.assertEqual(
            get_translations_reverse_relation(Country, 'continent'),
            'sample_continent__countries'
        )

    def test_nested_relation(self):
        """Make sure it works with a nested relation."""
        self.assertEqual(
            get_translations_reverse_relation(Continent, 'countries__cities'),
            'sample_city__country__continent'
        )

    def test_nested_reverse_relation(self):
        """Make sure it works with a nested relation in reverse."""
        self.assertEqual(
            get_translations_reverse_relation(City, 'country__continent'),
            'sample_continent__countries__cities'
        )

    def test_none_relation(self):
        """Make sure it works with None relation."""
        self.assertEqual(
            get_translations_reverse_relation(Continent),
            'sample_continent'
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

    # ---- error testing -----------------------------------------------------

    def test_invalid_lang(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        with self.assertRaises(ValueError) as error:
            get_translations(
                europe,
                lang="xx"
            )
        self.assertEqual(
            error.exception.args[0],
            "The language code `xx` is not supported."
        )

    def test_invalid_relation(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de", "tr"]
        )
        with self.assertRaises(FieldDoesNotExist) as error:
            get_translations(
                europe,
                'wrong',
                lang="de"
            )
        self.assertEqual(
            error.exception.args[0],
            "Continent has no field named 'wrong'"
        )

    def test_invalid_context(self):
        class Person:
            def __init__(self, name):
                self.name = name

            def __str__(self):
                return self.name

            def __repr__(self):
                return self.name

        behzad = Person('Behzad')
        with self.assertRaises(TypeError) as error:
            get_translations(
                behzad,
                lang="de"
            )
        self.assertEqual(
            error.exception.args[0],
            "`Behzad` is neither a model instance nor an iterable of model instances."
        )


class GetDictionaryTest(TestCase):

    def test_translations_none(self):
        europe = create_continent("europe")
        self.assertDictEqual(
            get_dictionary(europe.translations.all()),
            {}
        )

    def test_one_conent_type_one_object_id_one_field(self):
        europe = create_continent(
            "europe",
            fields=["name"],
            langs=["de"]
        )

        continent_ct_id = ContentType.objects.get_for_model(Continent).id
        europe_id = str(europe.id)

        self.assertDictEqual(
            get_dictionary(Translation.objects.all()),
            {
                continent_ct_id: {
                    europe_id: {
                        'name': 'Europa'
                    }
                }
            }
        )

    def test_multiple_conent_type_one_object_id_one_field(self):
        europe = create_continent(
            "europe",
            fields=["name"],
            langs=["de"]
        )
        germany = create_country(
            europe,
            "germany",
            fields=["name"],
            langs=["de"]
        )
        cologne = create_city(
            germany,
            "cologne",
            fields=["name"],
            langs=["de"]
        )

        continent_ct_id = ContentType.objects.get_for_model(Continent).id
        country_ct_id = ContentType.objects.get_for_model(Country).id
        city_ct_id = ContentType.objects.get_for_model(City).id

        europe_id = str(europe.id)
        germany_id = str(germany.id)
        cologne_id = str(cologne.id)

        self.assertDictEqual(
            get_dictionary(Translation.objects.all()),
            {
                continent_ct_id: {
                    europe_id: {
                        'name': 'Europa',
                    }
                },
                country_ct_id: {
                    germany_id: {
                        'name': 'Deutschland',
                    }
                },
                city_ct_id: {
                    cologne_id: {
                        'name': 'Köln',
                    }
                }
            }
        )

    def test_one_conent_type_multiple_object_id_one_field(self):
        europe = create_continent(
            "europe",
            fields=["name"],
            langs=["de"]
        )
        asia = create_continent(
            "asia",
            fields=["name"],
            langs=["de"]
        )

        continent_ct_id = ContentType.objects.get_for_model(Continent).id
        europe_id = str(europe.id)
        asia_id = str(asia.id)

        self.assertDictEqual(
            get_dictionary(Translation.objects.all()),
            {
                continent_ct_id: {
                    europe_id: {
                        'name': 'Europa',
                    },
                    asia_id: {
                        'name': 'Asien',
                    }
                },
            }
        )

    def test_one_conent_type_one_object_id_multiple_field(self):
        europe = create_continent(
            "europe",
            fields=["name", "denonym"],
            langs=["de"]
        )

        continent_ct_id = ContentType.objects.get_for_model(Continent).id
        europe_id = str(europe.id)

        self.assertDictEqual(
            get_dictionary(Translation.objects.all()),
            {
                continent_ct_id: {
                    europe_id: {
                        'name': 'Europa',
                        'denonym': 'Europäisch',
                    },
                },
            }
        )

    def test_multiple_conent_type_multiple_object_id_multiple_field(self):
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
        cologne = create_city(
            germany,
            "cologne",
            fields=["name", "denonym"],
            langs=["de"]
        )
        munich = create_city(
            germany,
            "munich",
            fields=["name", "denonym"],
            langs=["de"]
        )

        turkey = create_country(
            europe,
            "turkey",
            fields=["name", "denonym"],
            langs=["de"]
        )
        istanbul = create_city(
            turkey,
            "istanbul",
            fields=["name", "denonym"],
            langs=["de"]
        )
        izmir = create_city(
            turkey,
            "izmir",
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
        mumbai = create_city(
            india,
            "mumbai",
            fields=["name", "denonym"],
            langs=["de"]
        )
        new_delhi = create_city(
            india,
            "new delhi",
            fields=["name", "denonym"],
            langs=["de"]
        )

        south_korea = create_country(
            asia,
            "south korea",
            fields=["name", "denonym"],
            langs=["de"]
        )
        seoul = create_city(
            south_korea,
            "seoul",
            fields=["name", "denonym"],
            langs=["de"]
        )
        ulsan = create_city(
            south_korea,
            "ulsan",
            fields=["name", "denonym"],
            langs=["de"]
        )

        continent_ct_id = ContentType.objects.get_for_model(Continent).id
        country_ct_id = ContentType.objects.get_for_model(Country).id
        city_ct_id = ContentType.objects.get_for_model(City).id

        europe_id = str(europe.id)
        asia_id = str(asia.id)

        germany_id = str(germany.id)
        turkey_id = str(turkey.id)
        india_id = str(india.id)
        south_korea_id = str(south_korea.id)

        cologne_id = str(cologne.id)
        munich_id = str(munich.id)
        istanbul_id = str(istanbul.id)
        izmir_id = str(izmir.id)
        mumbai_id = str(mumbai.id)
        new_delhi_id = str(new_delhi.id)
        seoul_id = str(seoul.id)
        ulsan_id = str(ulsan.id)

        self.assertDictEqual(
            get_dictionary(Translation.objects.all()),
            {
                continent_ct_id: {
                    europe_id: {
                        'name': 'Europa',
                        'denonym': 'Europäisch',
                    },
                    asia_id: {
                        'name': 'Asien',
                        'denonym': 'Asiatisch',
                    },
                },
                country_ct_id: {
                    germany_id: {
                        'name': 'Deutschland',
                        'denonym': 'Deutsche',
                    },
                    turkey_id: {
                        'name': 'Türkei',
                        'denonym': 'Türke',
                    },
                    india_id: {
                        'name': 'Indien',
                        'denonym': 'Indisch',
                    },
                    south_korea_id: {
                        'name': 'Südkorea',
                        'denonym': 'Südkoreanisch',
                    },
                },
                city_ct_id: {
                    cologne_id: {
                        'name': 'Köln',
                        'denonym': 'Kölner',
                    },
                    munich_id: {
                        'name': 'München',
                        'denonym': 'Münchner',
                    },
                    istanbul_id: {
                        'name': 'Ïstanbul',
                        'denonym': 'Ïstanbulisch',
                    },
                    izmir_id: {
                        'name': 'Ïzmir',
                        'denonym': 'Ïzmirisch',
                    },
                    mumbai_id: {
                        'name': 'Mumbaï',
                        'denonym': 'Mumbäisch',
                    },
                    new_delhi_id: {
                        'name': 'Neu-Delhi',
                        'denonym': 'Neu-Delhisch',
                    },
                    seoul_id: {
                        'name': 'Seül',
                        'denonym': 'Seülisch',
                    },
                    ulsan_id: {
                        'name': 'Ulsän',
                        'denonym': 'Ulsänisch',
                    },
                }
            }
        )


class GetRelationsDetailsTest(TestCase):

    def test_no_relations(self):
        self.assertDictEqual(
            get_relations_details(),
            {}
        )

    def test_one_included_no_nested_relations(self):
        self.assertEqual(
            get_relations_details(
                'countries'
            ),
            {
                'countries': {
                    'included': True,
                    'relations': []
                }
            }
        )

    def test_many_included_no_nested_relations(self):
        self.assertEqual(
            get_relations_details(
                'countries',
                'unions'
            ),
            {
                'countries': {
                    'included': True,
                    'relations': []
                },
                'unions': {
                    'included': True,
                    'relations': []
                },
            }
        )

    def test_one_unincluded_one_nested_relation(self):
        self.assertEqual(
            get_relations_details(
                'countries__cities'
            ),
            {
                'countries': {
                    'included': False,
                    'relations': ['cities']
                }
            }
        )

    def test_many_unincluded_one_nested_relation(self):
        self.assertEqual(
            get_relations_details(
                'countries__cities',
                'unions__countries',
            ),
            {
                'countries': {
                    'included': False,
                    'relations': ['cities']
                },
                'unions': {
                    'included': False,
                    'relations': ['countries']
                }
            }
        )

    def test_one_uincluded_many_nested_relations(self):
        self.assertEqual(
            get_relations_details(
                'countries__cities',
                'countries__currency'
            ),
            {
                'countries': {
                    'included': False,
                    'relations': [
                        'cities',
                        'currency'
                    ]
                }
            }
        )

    def test_many_uincluded_many_nested_relations(self):
        self.assertEqual(
            get_relations_details(
                'countries__cities',
                'countries__currency',
                'unions__countries',
                'unions__currency'
            ),
            {
                'countries': {
                    'included': False,
                    'relations': [
                        'cities',
                        'currency'
                    ]
                },
                'unions': {
                    'included': False,
                    'relations': [
                        'countries',
                        'currency'
                    ]
                }
            }
        )

    def test_one_included_one_nested_relations(self):
        self.assertEqual(
            get_relations_details(
                'countries',
                'countries__cities'
            ),
            {
                'countries': {
                    'included': True,
                    'relations': [
                        'cities'
                    ]
                }
            }
        )

    def test_many_included_one_nested_relations(self):
        self.assertEqual(
            get_relations_details(
                'countries',
                'countries__cities',
                'unions',
                'unions__countries'
            ),
            {
                'countries': {
                    'included': True,
                    'relations': [
                        'cities'
                    ]
                },
                'unions': {
                    'included': True,
                    'relations': [
                        'countries'
                    ]
                },
            }
        )

    def test_one_included_many_nested_relations(self):
        self.assertEqual(
            get_relations_details(
                'countries',
                'countries__cities',
                'countries__currency'
            ),
            {
                'countries': {
                    'included': True,
                    'relations': [
                        'cities',
                        'currency'
                    ]
                }
            }
        )

    def test_many_included_many_nested_relations(self):
        self.assertEqual(
            get_relations_details(
                'countries',
                'countries__cities',
                'countries__currency',
                'unions',
                'unions__countries',
                'unions__currency'
            ),
            {
                'countries': {
                    'included': True,
                    'relations': [
                        'cities',
                        'currency'
                    ]
                },
                'unions': {
                    'included': True,
                    'relations': [
                        'countries',
                        'currency'
                    ]
                },
            }
        )
