from django.test import TestCase
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
    """Tests for get_translations."""

    def test_instance_with_no_relation_and_with_no_lang(self):
        europe = Continent.objects.create(
            code="EU", name="Europe", denonym="European"
        )

        asia = Continent.objects.create(
            code="AS", name="Asia", denonym="Asian"
        )

        europe.translations.create(
            field="name", language="de", text="Europa"
        )
        europe.translations.create(
            field="denonym", language="de", text="Europäisch"
        )
        europe.translations.create(
            field="name", language="tr", text="Avrupa"
        )
        europe.translations.create(
            field="denonym", language="tr", text="Avrupalı"
        )

        asia.translations.create(
            field="name", language="de", text="Asien"
        )
        asia.translations.create(
            field="denonym", language="de", text="Asiatisch"
        )
        asia.translations.create(
            field="name", language="tr", text="Asya"
        )
        asia.translations.create(
            field="denonym", language="tr", text="Asyalı"
        )

        activate("de")
        self.assertQuerysetEqual(
            get_translations(europe).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>"
            ]
        )
        self.assertQuerysetEqual(
            get_translations(asia).order_by("id"),
            [
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>"
            ]
        )

        activate("tr")
        self.assertQuerysetEqual(
            get_translations(europe).order_by("id"),
            [
                "<Translation: Europe: Avrupa>",
                "<Translation: European: Avrupalı>"
            ]
        )
        self.assertQuerysetEqual(
            get_translations(asia).order_by("id"),
            [
                "<Translation: Asia: Asya>",
                "<Translation: Asian: Asyalı>"
            ]
        )

    def test_instance_with_no_relation_and_with_lang(self):
        europe = Continent.objects.create(
            code="EU", name="Europe", denonym="European"
        )

        asia = Continent.objects.create(
            code="AS", name="Asia", denonym="Asian"
        )

        europe.translations.create(
            field="name", language="de", text="Europa"
        )
        europe.translations.create(
            field="denonym", language="de", text="Europäisch"
        )
        europe.translations.create(
            field="name", language="tr", text="Avrupa"
        )
        europe.translations.create(
            field="denonym", language="tr", text="Avrupalı"
        )

        asia.translations.create(
            field="name", language="de", text="Asien"
        )
        asia.translations.create(
            field="denonym", language="de", text="Asiatisch"
        )
        asia.translations.create(
            field="name", language="tr", text="Asya"
        )
        asia.translations.create(
            field="denonym", language="tr", text="Asyalı"
        )

        self.assertQuerysetEqual(
            get_translations(europe, lang="de").order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>"
            ]
        )
        self.assertQuerysetEqual(
            get_translations(asia, lang="de").order_by("id"),
            [
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>"
            ]
        )

        self.assertQuerysetEqual(
            get_translations(europe, lang="tr").order_by("id"),
            [
                "<Translation: Europe: Avrupa>",
                "<Translation: European: Avrupalı>"
            ]
        )
        self.assertQuerysetEqual(
            get_translations(asia, lang="tr").order_by("id"),
            [
                "<Translation: Asia: Asya>",
                "<Translation: Asian: Asyalı>"
            ]
        )

    def test_instance_with_relation_and_with_lang(self):
        europe = Continent.objects.create(
            code="EU", name="Europe", denonym="European"
        )
        germany = europe.countries.create(
            code="DE", name="Germany", denonym="German"
        )
        cologne = germany.cities.create(
            name="Cologne", denonym="Cologner"
        )

        asia = Continent.objects.create(
            code="AS", name="Asia", denonym="Asian"
        )
        persia = asia.countries.create(
            code="IR", name="Persia", denonym="Persian"
        )
        shiraz = persia.cities.create(
            name="Shiraz", denonym="Shirazer"
        )

        europe.translations.create(
            field="name", language="de", text="Europa"
        )
        europe.translations.create(
            field="denonym", language="de", text="Europäisch"
        )
        germany.translations.create(
            field="name", language="de", text="Deutschland"
        )
        germany.translations.create(
            field="denonym", language="de", text="Deutsche"
        )
        cologne.translations.create(
            field="name", language="de", text="Köln"
        )
        cologne.translations.create(
            field="denonym", language="de", text="Kölnisch"
        )
        europe.translations.create(
            field="name", language="tr", text="Avrupa"
        )
        europe.translations.create(
            field="denonym", language="tr", text="Avrupalı"
        )
        germany.translations.create(
            field="name", language="tr", text="Almanya"
        )
        germany.translations.create(
            field="denonym", language="tr", text="Almanca"
        )
        cologne.translations.create(
            field="name", language="tr", text="Koln"
        )
        cologne.translations.create(
            field="denonym", language="tr", text="Kolnlı"
        )

        asia.translations.create(
            field="name", language="de", text="Asien"
        )
        asia.translations.create(
            field="denonym", language="de", text="Asiatisch"
        )
        persia.translations.create(
            field="name", language="de", text="Persien"
        )
        persia.translations.create(
            field="denonym", language="de", text="Persisch"
        )
        shiraz.translations.create(
            field="name", language="de", text="Schiras"
        )
        shiraz.translations.create(
            field="denonym", language="de", text="Schirasisch"
        )
        asia.translations.create(
            field="name", language="tr", text="Asya"
        )
        asia.translations.create(
            field="denonym", language="tr", text="Asyalı"
        )
        persia.translations.create(
            field="name", language="tr", text="İran"
        )
        persia.translations.create(
            field="denonym", language="tr", text="İranlı"
        )
        shiraz.translations.create(
            field="name", language="tr", text="Şiraz"
        )
        shiraz.translations.create(
            field="denonym", language="tr", text="Şirazlı"
        )

        self.assertQuerysetEqual(
            get_translations(
                europe, lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>"
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                europe, "countries", lang="de"
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
                europe, "countries", "countries__cities", lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
                "<Translation: Cologne: Köln>",
                "<Translation: Cologner: Kölnisch>",
            ]
        )

        self.assertQuerysetEqual(
            get_translations(
                asia, lang="de"
            ).order_by("id"),
            [
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>"
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                asia, "countries", lang="de"
            ).order_by("id"),
            [
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: Persia: Persien>",
                "<Translation: Persian: Persisch>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                asia, "countries", "countries__cities", lang="de"
            ).order_by("id"),
            [
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: Persia: Persien>",
                "<Translation: Persian: Persisch>",
                "<Translation: Shiraz: Schiras>",
                "<Translation: Shirazer: Schirasisch>",
            ]
        )

        self.assertQuerysetEqual(
            get_translations(
                europe, lang="tr"
            ).order_by("id"),
            [
                "<Translation: Europe: Avrupa>",
                "<Translation: European: Avrupalı>"
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                europe, "countries", lang="tr"
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
                europe, "countries", "countries__cities", lang="tr"
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
                asia, lang="tr"
            ).order_by("id"),
            [
                "<Translation: Asia: Asya>",
                "<Translation: Asian: Asyalı>"
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                asia, "countries", lang="tr"
            ).order_by("id"),
            [
                "<Translation: Asia: Asya>",
                "<Translation: Asian: Asyalı>",
                "<Translation: Persia: İran>",
                "<Translation: Persian: İranlı>",
            ]
        )
        self.assertQuerysetEqual(
            get_translations(
                asia, "countries", "countries__cities", lang="tr"
            ).order_by("id"),
            [
                "<Translation: Asia: Asya>",
                "<Translation: Asian: Asyalı>",
                "<Translation: Persia: İran>",
                "<Translation: Persian: İranlı>",
                "<Translation: Shiraz: Şiraz>",
                "<Translation: Shirazer: Şirazlı>",
            ]
        )
