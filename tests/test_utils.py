from django.test import TestCase
from django.db import models
from django.core.exceptions import FieldDoesNotExist
from django.utils.translation import activate, deactivate
from django.contrib.contenttypes.models import ContentType

from translations.utils import _get_translation_language, \
    _get_entity_details, _get_reverse_relation, \
    _get_translations_reverse_relation, _get_translations, \
    _get_translations_dictionary, _fill_hierarchy, _get_relations_hierarchy, \
    _apply_obj_translations, _apply_rel_translations, \
    _apply_entity_translations, apply_translations

from translations.models import Translation

from sample.models import Continent, Country, City

from .sample import create_samples


class GetTranslationLanguageTest(TestCase):
    """Tests for `_get_translation_language`."""

    def test_active_lang(self):
        """Make sure it works with an active language."""
        activate('en')
        self.assertEqual(
            _get_translation_language(),
            'en'
        )

    def test_custom_lang(self):
        """Make sure it works with a valid language code."""
        self.assertEqual(
            _get_translation_language('de'),
            'de'
        )

    def test_invalid_lang(self):
        """Make sure it raises on an invalid language code."""
        with self.assertRaises(ValueError) as error:
            _get_translation_language('xx')
        self.assertEqual(
            error.exception.args[0],
            "The language code `xx` is not supported."
        )


class GetEntityDetailsTest(TestCase):
    """Tests for `_get_entity_details`."""

    def test_iterable(self):
        """Make sure it works with a model iterable."""
        create_samples(continent_names=["europe", "asia"])

        continents = list(Continent.objects.all())
        self.assertEqual(
            _get_entity_details(continents),
            (True, Continent)
        )

    def test_queryset(self):
        """Make sure it works with a model queryset."""
        create_samples(continent_names=["europe", "asia"])

        continents = Continent.objects.all()
        self.assertEqual(
            _get_entity_details(continents),
            (True, Continent)
        )

    def test_instance(self):
        """Make sure it works with a model instance."""
        create_samples(continent_names=["europe"])

        europe = Continent.objects.get(code="EU")

        self.assertEqual(
            _get_entity_details(europe),
            (False, Continent)
        )

    def test_empty_iterable(self):
        """Make sure it works with an empty list."""
        self.assertEqual(
            _get_entity_details([]),
            (True, None)
        )

    def test_empty_queryset(self):
        """Make sure it works with an empty queryset."""
        continents = Continent.objects.none()
        self.assertEqual(
            _get_entity_details(continents),
            (True, None)
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
            _get_entity_details(people)
        self.assertEqual(
            error.exception.args[0],
            "`[Behzad, Max]` is neither a model instance nor an iterable of model instances."
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
            _get_entity_details(behzad)
        self.assertEqual(
            error.exception.args[0],
            "`Behzad` is neither a model instance nor an iterable of model instances."
        )


class GetReverseRelationTest(TestCase):
    """Tests for `_get_reverse_relation`."""

    def test_simple_relation(self):
        """Make sure it works with a simple relation."""
        self.assertEqual(
            _get_reverse_relation(Continent, 'countries'),
            'continent'
        )

    def test_simple_reverse_relation(self):
        """Make sure it works with a simple relation in reverse."""
        self.assertEqual(
            _get_reverse_relation(Country, 'continent'),
            'countries'
        )

    def test_nested_relation(self):
        """Make sure it works with a nested relation."""
        self.assertEqual(
            _get_reverse_relation(Continent, 'countries__cities'),
            'country__continent'
        )

    def test_nested_reverse_relation(self):
        """Make sure it works with a nested relation in reverse."""
        self.assertEqual(
            _get_reverse_relation(City, 'country__continent'),
            'countries__cities'
        )

    def test_empty_relation(self):
        """Make sure it raises on an empty relation."""
        with self.assertRaises(FieldDoesNotExist) as error:
            _get_reverse_relation(
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
            _get_reverse_relation(
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
            _get_reverse_relation(
                Continent,
                'countries__wrong'
            )
        self.assertEqual(
            error.exception.args[0],
            "Country has no field named 'wrong'"
        )


class GetTranslationsReverseRelationTest(TestCase):
    """Tests for `_get_translations_reverse_relation`."""

    def test_simple_relation(self):
        """Make sure it works with a simple relation."""
        self.assertEqual(
            _get_translations_reverse_relation(Continent, 'countries'),
            'sample_country__continent'
        )

    def test_simple_reverse_relation(self):
        """Make sure it works with a simple relation in reverse."""
        self.assertEqual(
            _get_translations_reverse_relation(Country, 'continent'),
            'sample_continent__countries'
        )

    def test_nested_relation(self):
        """Make sure it works with a nested relation."""
        self.assertEqual(
            _get_translations_reverse_relation(Continent, 'countries__cities'),
            'sample_city__country__continent'
        )

    def test_nested_reverse_relation(self):
        """Make sure it works with a nested relation in reverse."""
        self.assertEqual(
            _get_translations_reverse_relation(City, 'country__continent'),
            'sample_continent__countries__cities'
        )

    def test_none_relation(self):
        """Make sure it works with None relation."""
        self.assertEqual(
            _get_translations_reverse_relation(Continent),
            'sample_continent'
        )

    def test_empty_relation(self):
        """Make sure it raises on an empty relation."""
        with self.assertRaises(FieldDoesNotExist) as error:
            _get_translations_reverse_relation(
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
            _get_translations_reverse_relation(
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
            _get_translations_reverse_relation(
                Continent,
                'countries__wrong'
            )
        self.assertEqual(
            error.exception.args[0],
            "Country has no field named 'wrong'"
        )


class GetTranslationsTest(TestCase):
    """Tests for `_get_translations`."""

    # ---- arguments testing -------------------------------------------------

    def test_instance_level_0_relation_no_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        europe = Continent.objects.get(code="EU")

        activate("de")
        self.assertQuerysetEqual(
            _get_translations(
                europe
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
            ]
        )

    def test_instance_level_1_relation_no_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        europe = Continent.objects.get(code="EU")

        activate("de")
        self.assertQuerysetEqual(
            _get_translations(
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

    def test_instance_level_2_relation_no_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        europe = Continent.objects.get(code="EU")

        activate("de")
        self.assertQuerysetEqual(
            _get_translations(
                europe,
                "countries__cities"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Cologne: Köln>",
                "<Translation: Cologner: Kölner>",
            ]
        )

    def test_instance_level_1_2_relation_no_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        europe = Continent.objects.get(code="EU")

        activate("de")
        self.assertQuerysetEqual(
            _get_translations(
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

    def test_instance_level_0_relation_with_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        europe = Continent.objects.get(code="EU")

        self.assertQuerysetEqual(
            _get_translations(
                europe,
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
            ]
        )

    def test_instance_level_1_relation_with_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        europe = Continent.objects.get(code="EU")

        self.assertQuerysetEqual(
            _get_translations(
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

    def test_instance_level_2_relation_with_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        europe = Continent.objects.get(code="EU")

        self.assertQuerysetEqual(
            _get_translations(
                europe,
                "countries__cities",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Cologne: Köln>",
                "<Translation: Cologner: Kölner>",
            ]
        )

    def test_instance_level_1_2_relation_with_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        europe = Continent.objects.get(code="EU")

        self.assertQuerysetEqual(
            _get_translations(
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

    def test_queryset_level_0_relation_no_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        continents = Continent.objects.all()

        activate("de")
        self.assertQuerysetEqual(
            _get_translations(
                continents
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
            ]
        )

    def test_queryset_level_1_relation_no_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        continents = Continent.objects.all()

        activate("de")
        self.assertQuerysetEqual(
            _get_translations(
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
                "<Translation: South Korea: Südkorea>",
                "<Translation: South Korean: Südkoreanisch>",
            ]
        )

    def test_queryset_level_2_relation_no_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        continents = Continent.objects.all()

        activate("de")
        self.assertQuerysetEqual(
            _get_translations(
                continents,
                "countries__cities"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Cologne: Köln>",
                "<Translation: Cologner: Kölner>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: Seoul: Seül>",
                "<Translation: Seouler: Seüler>",
            ]
        )

    def test_queryset_level_1_2_relation_no_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        continents = Continent.objects.all()

        activate("de")
        self.assertQuerysetEqual(
            _get_translations(
                continents,
                "countries",
                "countries__cities"
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
                "<Translation: South Korea: Südkorea>",
                "<Translation: South Korean: Südkoreanisch>",
                "<Translation: Seoul: Seül>",
                "<Translation: Seouler: Seüler>",
            ]
        )

    def test_queryset_level_0_relation_with_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        continents = Continent.objects.all()

        self.assertQuerysetEqual(
            _get_translations(
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

    def test_queryset_level_1_relation_with_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        continents = Continent.objects.all()

        self.assertQuerysetEqual(
            _get_translations(
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
                "<Translation: South Korea: Südkorea>",
                "<Translation: South Korean: Südkoreanisch>",
            ]
        )

    def test_queryset_level_2_relation_with_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        continents = Continent.objects.all()

        self.assertQuerysetEqual(
            _get_translations(
                continents,
                "countries__cities",
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Cologne: Köln>",
                "<Translation: Cologner: Kölner>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: Seoul: Seül>",
                "<Translation: Seouler: Seüler>",
            ]
        )

    def test_queryset_level_1_2_relation_with_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        continents = Continent.objects.all()

        self.assertQuerysetEqual(
            _get_translations(
                continents,
                "countries",
                "countries__cities",
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
                "<Translation: South Korea: Südkorea>",
                "<Translation: South Korean: Südkoreanisch>",
                "<Translation: Seoul: Seül>",
                "<Translation: Seouler: Seüler>",
            ]
        )

    # ---- error testing -----------------------------------------------------

    def test_invalid_lang(self):
        create_samples(
            continent_names=["europe"],
            continent_fields=["name", "denonym"],
            langs=["de"]
        )

        europe = Continent.objects.get(code="EU")

        with self.assertRaises(ValueError) as error:
            _get_translations(
                europe,
                lang="xx"
            )
        self.assertEqual(
            error.exception.args[0],
            "The language code `xx` is not supported."
        )

    def test_invalid_relation(self):
        create_samples(
            continent_names=["europe"],
            continent_fields=["name", "denonym"],
            langs=["de"]
        )

        europe = Continent.objects.get(code="EU")

        with self.assertRaises(FieldDoesNotExist) as error:
            _get_translations(
                europe,
                'wrong',
                lang="de"
            )
        self.assertEqual(
            error.exception.args[0],
            "Continent has no field named 'wrong'"
        )

    def test_invalid_entity(self):
        class Person:
            def __init__(self, name):
                self.name = name

            def __str__(self):
                return self.name

            def __repr__(self):
                return self.name

        behzad = Person('Behzad')
        with self.assertRaises(TypeError) as error:
            _get_translations(
                behzad,
                lang="de"
            )
        self.assertEqual(
            error.exception.args[0],
            "`Behzad` is neither a model instance nor an iterable of model instances."
        )


class GetTranslationsDictionaryTest(TestCase):
    """Tests for `_get_translations_dictionary`."""

    def test_none(self):
        self.assertDictEqual(
            _get_translations_dictionary(Translation.objects.none()),
            {}
        )

    def test_one_conent_type_one_object_id_one_field(self):
        create_samples(
            continent_names=["europe"],
            continent_fields=["name"],
            langs=["de"]
        )

        europe = Continent.objects.get(code="EU")

        continent_ct_id = ContentType.objects.get_for_model(Continent).id
        europe_id = str(europe.id)

        self.assertDictEqual(
            _get_translations_dictionary(Translation.objects.all()),
            {
                continent_ct_id: {
                    europe_id: {
                        'name': 'Europa'
                    }
                }
            }
        )

    def test_multiple_conent_type_one_object_id_one_field(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name"],
            country_fields=["name"],
            city_fields=["name"],
            langs=["de"]
        )

        europe = Continent.objects.get(code="EU")
        germany = Country.objects.get(code="DE")
        cologne = City.objects.get(name="Cologne")

        continent_ct_id = ContentType.objects.get_for_model(Continent).id
        country_ct_id = ContentType.objects.get_for_model(Country).id
        city_ct_id = ContentType.objects.get_for_model(City).id

        europe_id = str(europe.id)
        germany_id = str(germany.id)
        cologne_id = str(cologne.id)

        self.assertDictEqual(
            _get_translations_dictionary(Translation.objects.all()),
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
        create_samples(
            continent_names=["europe", "asia"],
            continent_fields=["name"],
            langs=["de"]
        )

        europe = Continent.objects.get(code="EU")
        asia = Continent.objects.get(code="AS")

        continent_ct_id = ContentType.objects.get_for_model(Continent).id
        europe_id = str(europe.id)
        asia_id = str(asia.id)

        self.assertDictEqual(
            _get_translations_dictionary(Translation.objects.all()),
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
        create_samples(
            continent_names=["europe"],
            continent_fields=["name", "denonym"],
            langs=["de"]
        )

        europe = Continent.objects.get(code="EU")

        continent_ct_id = ContentType.objects.get_for_model(Continent).id
        europe_id = str(europe.id)

        self.assertDictEqual(
            _get_translations_dictionary(Translation.objects.all()),
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
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "turkey", "india", "south korea"],
            city_names=[
                "cologne", "munich", "istanbul", "izmir",
                "mumbai", "new delhi", "seoul", "ulsan",
            ],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        europe = Continent.objects.get(code="EU")
        asia = Continent.objects.get(code="AS")

        germany = Country.objects.get(code="DE")
        turkey = Country.objects.get(code="TR")
        india = Country.objects.get(code="IN")
        south_korea = Country.objects.get(code="KR")

        cologne = City.objects.get(name="Cologne")
        munich = City.objects.get(name="Munich")
        istanbul = City.objects.get(name="Istanbul")
        izmir = City.objects.get(name="Izmir")
        mumbai = City.objects.get(name="Mumbai")
        new_delhi = City.objects.get(name="New Delhi")
        seoul = City.objects.get(name="Seoul")
        ulsan = City.objects.get(name="Ulsan")

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
            _get_translations_dictionary(Translation.objects.all()),
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
                        'denonym': 'Seüler',
                    },
                    ulsan_id: {
                        'name': 'Ulsän',
                        'denonym': 'Ulsänisch',
                    },
                }
            }
        )


class FillHierarchyTest(TestCase):
    """Tests for `_fill_hierarchy`."""

    def test_one_included_no_nested_relations(self):
        hierarchy = {}
        _fill_hierarchy(hierarchy, 'countries')
        self.assertEqual(
            hierarchy,
            {
                'countries': {
                    'included': True,
                    'relations': {}
                }
            }
        )

    def test_many_included_no_nested_relations(self):
        hierarchy = {}
        _fill_hierarchy(hierarchy, 'countries')
        _fill_hierarchy(hierarchy, 'unions')
        self.assertEqual(
            hierarchy,
            {
                'countries': {
                    'included': True,
                    'relations': {}
                },
                'unions': {
                    'included': True,
                    'relations': {}
                },
            }
        )

    def test_one_unincluded_one_nested_relation(self):
        hierarchy = {}
        _fill_hierarchy(hierarchy, 'countries', 'cities')
        self.assertEqual(
            hierarchy,
            {
                'countries': {
                    'included': False,
                    'relations': {
                        'cities': {
                            'included': True,
                            'relations': {}
                        }
                    }
                }
            }
        )

    def test_many_unincluded_one_nested_relation(self):
        hierarchy = {}
        _fill_hierarchy(hierarchy, 'countries', 'cities')
        _fill_hierarchy(hierarchy, 'unions', 'projects')
        self.assertEqual(
            hierarchy,
            {
                'countries': {
                    'included': False,
                    'relations': {
                        'cities': {
                            'included': True,
                            'relations': {}
                        }
                    }
                },
                'unions': {
                    'included': False,
                    'relations': {
                        'projects': {
                            'included': True,
                            'relations': {}
                        }
                    }
                }
            }
        )

    def test_one_uincluded_many_nested_relations(self):
        hierarchy = {}
        _fill_hierarchy(hierarchy, 'countries', 'cities')
        _fill_hierarchy(hierarchy, 'countries', 'currency')
        self.assertEqual(
            hierarchy,
            {
                'countries': {
                    'included': False,
                    'relations': {
                        'cities': {
                            'included': True,
                            'relations': {}
                        },
                        'currency': {
                            'included': True,
                            'relations': {}
                        }
                    }
                }
            }
        )

    def test_many_uincluded_many_nested_relations(self):
        hierarchy = {}
        _fill_hierarchy(hierarchy, 'countries', 'cities')
        _fill_hierarchy(hierarchy, 'countries', 'currency')
        _fill_hierarchy(hierarchy, 'unions', 'projects')
        _fill_hierarchy(hierarchy, 'unions', 'currency')
        self.assertEqual(
            hierarchy,
            {
                'countries': {
                    'included': False,
                    'relations': {
                        'cities': {
                            'included': True,
                            'relations': {}
                        },
                        'currency': {
                            'included': True,
                            'relations': {}
                        }
                    }
                },
                'unions': {
                    'included': False,
                    'relations': {
                        'projects': {
                            'included': True,
                            'relations': {}
                        },
                        'currency': {
                            'included': True,
                            'relations': {}
                        }
                    }
                }
            }
        )

    def test_one_included_one_nested_relations(self):
        hierarchy = {}
        _fill_hierarchy(hierarchy, 'countries')
        _fill_hierarchy(hierarchy, 'countries', 'cities')
        self.assertEqual(
            hierarchy,
            {
                'countries': {
                    'included': True,
                    'relations': {
                        'cities': {
                            'included': True,
                            'relations': {}
                        }
                    }
                }
            }
        )

    def test_many_included_one_nested_relations(self):
        hierarchy = {}
        _fill_hierarchy(hierarchy, 'countries')
        _fill_hierarchy(hierarchy, 'countries', 'cities')
        _fill_hierarchy(hierarchy, 'unions')
        _fill_hierarchy(hierarchy, 'unions', 'projects')
        self.assertEqual(
            hierarchy,
            {
                'countries': {
                    'included': True,
                    'relations': {
                        'cities': {
                            'included': True,
                            'relations': {}
                        }
                    }
                },
                'unions': {
                    'included': True,
                    'relations': {
                        'projects': {
                            'included': True,
                            'relations': {}
                        }
                    }
                },
            }
        )

    def test_one_included_many_nested_relations(self):
        hierarchy = {}
        _fill_hierarchy(hierarchy, 'countries')
        _fill_hierarchy(hierarchy, 'countries', 'cities')
        _fill_hierarchy(hierarchy, 'countries', 'currency')
        self.assertEqual(
            hierarchy,
            {
                'countries': {
                    'included': True,
                    'relations': {
                        'cities': {
                            'included': True,
                            'relations': {}
                        },
                        'currency': {
                            'included': True,
                            'relations': {}
                        }
                    }
                }
            }
        )

    def test_many_included_many_nested_relations(self):
        hierarchy = {}
        _fill_hierarchy(hierarchy, 'countries')
        _fill_hierarchy(hierarchy, 'countries', 'cities')
        _fill_hierarchy(hierarchy, 'countries', 'currency')
        _fill_hierarchy(hierarchy, 'unions')
        _fill_hierarchy(hierarchy, 'unions', 'projects')
        _fill_hierarchy(hierarchy, 'unions', 'currency')
        self.assertEqual(
            hierarchy,
            {
                'countries': {
                    'included': True,
                    'relations': {
                        'cities': {
                            'included': True,
                            'relations': {}
                        },
                        'currency': {
                            'included': True,
                            'relations': {}
                        }
                    }
                },
                'unions': {
                    'included': True,
                    'relations': {
                        'projects': {
                            'included': True,
                            'relations': {}
                        },
                        'currency': {
                            'included': True,
                            'relations': {}
                        }
                    }
                },
            }
        )


class GetRelationsHierarchyTest(TestCase):
    """Tests for `_get_relations_hierarchy`."""

    def test_no_relations(self):
        self.assertDictEqual(
            _get_relations_hierarchy(),
            {}
        )

    def test_one_included_no_nested_relations(self):
        self.assertEqual(
            _get_relations_hierarchy(
                'countries'
            ),
            {
                'countries': {
                    'included': True,
                    'relations': {}
                }
            }
        )

    def test_many_included_no_nested_relations(self):
        self.assertEqual(
            _get_relations_hierarchy(
                'countries',
                'unions'
            ),
            {
                'countries': {
                    'included': True,
                    'relations': {}
                },
                'unions': {
                    'included': True,
                    'relations': {}
                },
            }
        )

    def test_one_unincluded_one_nested_relation(self):
        self.assertEqual(
            _get_relations_hierarchy(
                'countries__cities'
            ),
            {
                'countries': {
                    'included': False,
                    'relations': {
                        'cities': {
                            'included': True,
                            'relations': {}
                        }
                    }
                }
            }
        )

    def test_many_unincluded_one_nested_relation(self):
        self.assertEqual(
            _get_relations_hierarchy(
                'countries__cities',
                'unions__projects',
            ),
            {
                'countries': {
                    'included': False,
                    'relations': {
                        'cities': {
                            'included': True,
                            'relations': {}
                        }
                    }
                },
                'unions': {
                    'included': False,
                    'relations': {
                        'projects': {
                            'included': True,
                            'relations': {}
                        }
                    }
                }
            }
        )

    def test_one_uincluded_many_nested_relations(self):
        self.assertEqual(
            _get_relations_hierarchy(
                'countries__cities',
                'countries__currency'
            ),
            {
                'countries': {
                    'included': False,
                    'relations': {
                        'cities': {
                            'included': True,
                            'relations': {}
                        },
                        'currency': {
                            'included': True,
                            'relations': {}
                        }
                    }
                }
            }
        )

    def test_many_uincluded_many_nested_relations(self):
        self.assertEqual(
            _get_relations_hierarchy(
                'countries__cities',
                'countries__currency',
                'unions__projects',
                'unions__currency'
            ),
            {
                'countries': {
                    'included': False,
                    'relations': {
                        'cities': {
                            'included': True,
                            'relations': {}
                        },
                        'currency': {
                            'included': True,
                            'relations': {}
                        }
                    }
                },
                'unions': {
                    'included': False,
                    'relations': {
                        'projects': {
                            'included': True,
                            'relations': {}
                        },
                        'currency': {
                            'included': True,
                            'relations': {}
                        }
                    }
                }
            }
        )

    def test_one_included_one_nested_relations(self):
        self.assertEqual(
            _get_relations_hierarchy(
                'countries',
                'countries__cities'
            ),
            {
                'countries': {
                    'included': True,
                    'relations': {
                        'cities': {
                            'included': True,
                            'relations': {}
                        }
                    }
                }
            }
        )

    def test_many_included_one_nested_relations(self):
        self.assertEqual(
            _get_relations_hierarchy(
                'countries',
                'countries__cities',
                'unions',
                'unions__projects'
            ),
            {
                'countries': {
                    'included': True,
                    'relations': {
                        'cities': {
                            'included': True,
                            'relations': {}
                        }
                    }
                },
                'unions': {
                    'included': True,
                    'relations': {
                        'projects': {
                            'included': True,
                            'relations': {}
                        }
                    }
                },
            }
        )

    def test_one_included_many_nested_relations(self):
        self.assertEqual(
            _get_relations_hierarchy(
                'countries',
                'countries__cities',
                'countries__currency'
            ),
            {
                'countries': {
                    'included': True,
                    'relations': {
                        'cities': {
                            'included': True,
                            'relations': {}
                        },
                        'currency': {
                            'included': True,
                            'relations': {}
                        }
                    }
                }
            }
        )

    def test_many_included_many_nested_relations(self):
        self.assertEqual(
            _get_relations_hierarchy(
                'countries',
                'countries__cities',
                'countries__currency',
                'unions',
                'unions__projects',
                'unions__currency'
            ),
            {
                'countries': {
                    'included': True,
                    'relations': {
                        'cities': {
                            'included': True,
                            'relations': {}
                        },
                        'currency': {
                            'included': True,
                            'relations': {}
                        }
                    }
                },
                'unions': {
                    'included': True,
                    'relations': {
                        'projects': {
                            'included': True,
                            'relations': {}
                        },
                        'currency': {
                            'included': True,
                            'relations': {}
                        }
                    }
                },
            }
        )


class ApplyObjTranslations(TestCase):
    """Tests for `_apply_obj_translations`."""

    def test_empty_ct_dictionary(self):
        create_samples(continent_names=["europe"])

        europe = Continent.objects.get(code="EU")
        fields = Continent.get_translatable_fields()
        translations = _get_translations(europe, lang="de")
        dictionary = _get_translations_dictionary(translations)
        europe_ct = ContentType.objects.get_for_model(europe)
        ct_dictionary = dictionary.get(europe_ct.id, {})

        _apply_obj_translations(europe, fields, ct_dictionary, included=True)

        self.assertEqual(
            europe.name,
            "Europe"
        )
        self.assertEqual(
            europe.denonym,
            "European"
        )

    def test_ct_dictionary(self):
        create_samples(
            continent_names=["europe"],
            continent_fields=["name", "denonym"],
            langs=["de"]
        )

        europe = Continent.objects.get(code="EU")
        fields = Continent.get_translatable_fields()
        translations = _get_translations(europe, lang="de")
        dictionary = _get_translations_dictionary(translations)
        europe_ct = ContentType.objects.get_for_model(europe)
        ct_dictionary = dictionary[europe_ct.id]

        _apply_obj_translations(europe, fields, ct_dictionary, included=True)

        self.assertEqual(
            europe.name,
            "Europa"
        )
        self.assertEqual(
            europe.denonym,
            "Europäisch"
        )

    def test_included(self):
        create_samples(
            continent_names=["europe"],
            continent_fields=["name", "denonym"],
            langs=["de"]
        )

        europe = Continent.objects.get(code="EU")
        fields = Continent.get_translatable_fields()
        translations = _get_translations(europe, lang="de")
        dictionary = _get_translations_dictionary(translations)
        europe_ct = ContentType.objects.get_for_model(europe)
        ct_dictionary = dictionary[europe_ct.id]

        _apply_obj_translations(europe, fields, ct_dictionary, included=False)

        self.assertEqual(
            europe.name,
            "Europe"
        )
        self.assertEqual(
            europe.denonym,
            "European"
        )


class ApplyRelTranslations(TestCase):
    """Tests for `_apply_rel_translations`."""

    def test_level_0_hierarchy_level_0_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy()

        _apply_rel_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_0_hierarchy_level_1_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_1, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy()

        _apply_rel_translations(europe, {}, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_0_hierarchy_level_2_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_2 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_2, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy()

        _apply_rel_translations(europe, {}, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_0_hierarchy_level_1_2_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_1_2, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy()

        _apply_rel_translations(europe, {}, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_1_hierarchy_level_0_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_1)

        _apply_rel_translations(europe, hierarchy, {})

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_1_hierarchy_level_1_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_1, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_1)

        _apply_rel_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_1_hierarchy_level_2_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1 = ('countries',)
        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_2, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_1)

        _apply_rel_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_1_hierarchy_level_1_2_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_1_2, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_1)

        _apply_rel_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_2_hierarchy_level_0_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_2)

        _apply_rel_translations(europe, hierarchy, {})

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_2_hierarchy_level_1_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1 = ('countries',)
        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_1, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_2)

        _apply_rel_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_2_hierarchy_level_2_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_2, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_2)

        _apply_rel_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )

    def test_level_2_hierarchy_level_1_2_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_1_2, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_2)

        _apply_rel_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )

    def test_level_1_2_hierarchy_level_0_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_1_2)

        _apply_rel_translations(europe, hierarchy, {})

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_1_2_hierarchy_level_1_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_1, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_1_2)

        _apply_rel_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_1_2_hierarchy_level_2_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_2, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_1_2)

        _apply_rel_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )

    def test_level_1_2_hierarchy_level_1_2_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_1_2, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_1_2)

        _apply_rel_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )


class ApplyEntityTranslations(TestCase):
    """Tests for `_apply_entity_translations`."""

    def test_level_0_hierarchy_level_0_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy()

        _apply_entity_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_0_hierarchy_level_1_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_1, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy()

        _apply_entity_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_0_hierarchy_level_2_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_2 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_2, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy()

        _apply_entity_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_0_hierarchy_level_1_2_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_1_2, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy()

        _apply_entity_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_1_hierarchy_level_0_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_1)

        _apply_entity_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_1_hierarchy_level_1_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_1, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_1)

        _apply_entity_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_1_hierarchy_level_2_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1 = ('countries',)
        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_2, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_1)

        _apply_entity_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_1_hierarchy_level_1_2_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_1_2, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_1)

        _apply_entity_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_2_hierarchy_level_0_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_2)

        _apply_entity_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_2_hierarchy_level_1_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1 = ('countries',)
        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_1, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_2)

        _apply_entity_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_2_hierarchy_level_2_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_2, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_2)

        _apply_entity_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )

    def test_level_2_hierarchy_level_1_2_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_1_2, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_2)

        _apply_entity_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )

    def test_level_1_2_hierarchy_level_0_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_1_2)

        _apply_entity_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_1_2_hierarchy_level_1_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_1, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_1_2)

        _apply_entity_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_1_2_hierarchy_level_2_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_2, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_1_2)

        _apply_entity_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )

    def test_level_1_2_hierarchy_level_1_2_dictionary(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_1_2, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_1_2)

        _apply_entity_translations(europe, hierarchy, dictionary)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )

    def test_level_0_hierarchy_level_0_dictionary_unincluded(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy()

        _apply_entity_translations(europe, hierarchy, dictionary, included=False)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe'
        )
        self.assertEqual(
            europe.denonym,
            'European'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_0_hierarchy_level_1_dictionary_unincluded(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_1, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy()

        _apply_entity_translations(europe, hierarchy, dictionary, included=False)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe'
        )
        self.assertEqual(
            europe.denonym,
            'European'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_0_hierarchy_level_2_dictionary_unincluded(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_2 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_2, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy()

        _apply_entity_translations(europe, hierarchy, dictionary, included=False)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe'
        )
        self.assertEqual(
            europe.denonym,
            'European'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_0_hierarchy_level_1_2_dictionary_unincluded(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_1_2, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy()

        _apply_entity_translations(europe, hierarchy, dictionary, included=False)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe'
        )
        self.assertEqual(
            europe.denonym,
            'European'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_1_hierarchy_level_0_dictionary_unincluded(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_1)

        _apply_entity_translations(europe, hierarchy, dictionary, included=False)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe'
        )
        self.assertEqual(
            europe.denonym,
            'European'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_1_hierarchy_level_1_dictionary_unincluded(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_1, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_1)

        _apply_entity_translations(europe, hierarchy, dictionary, included=False)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe'
        )
        self.assertEqual(
            europe.denonym,
            'European'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_1_hierarchy_level_2_dictionary_unincluded(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1 = ('countries',)
        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_2, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_1)

        _apply_entity_translations(europe, hierarchy, dictionary, included=False)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe'
        )
        self.assertEqual(
            europe.denonym,
            'European'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_1_hierarchy_level_1_2_dictionary_unincluded(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_1_2, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_1)

        _apply_entity_translations(europe, hierarchy, dictionary, included=False)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe'
        )
        self.assertEqual(
            europe.denonym,
            'European'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_2_hierarchy_level_0_dictionary_unincluded(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_2)

        _apply_entity_translations(europe, hierarchy, dictionary, included=False)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe'
        )
        self.assertEqual(
            europe.denonym,
            'European'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_2_hierarchy_level_1_dictionary_unincluded(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1 = ('countries',)
        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_1, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_2)

        _apply_entity_translations(europe, hierarchy, dictionary, included=False)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe'
        )
        self.assertEqual(
            europe.denonym,
            'European'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_2_hierarchy_level_2_dictionary_unincluded(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_2, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_2)

        _apply_entity_translations(europe, hierarchy, dictionary, included=False)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe'
        )
        self.assertEqual(
            europe.denonym,
            'European'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )

    def test_level_2_hierarchy_level_1_2_dictionary_unincluded(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_1_2, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_2)

        _apply_entity_translations(europe, hierarchy, dictionary, included=False)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe'
        )
        self.assertEqual(
            europe.denonym,
            'European'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )

    def test_level_1_2_hierarchy_level_0_dictionary_unincluded(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_1_2)

        _apply_entity_translations(europe, hierarchy, dictionary, included=False)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe'
        )
        self.assertEqual(
            europe.denonym,
            'European'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_1_2_hierarchy_level_1_dictionary_unincluded(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_1, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_1_2)

        _apply_entity_translations(europe, hierarchy, dictionary, included=False)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe'
        )
        self.assertEqual(
            europe.denonym,
            'European'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_level_1_2_hierarchy_level_2_dictionary_unincluded(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_2, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_1_2)

        _apply_entity_translations(europe, hierarchy, dictionary, included=False)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe'
        )
        self.assertEqual(
            europe.denonym,
            'European'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )

    def test_level_1_2_hierarchy_level_1_2_dictionary_unincluded(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de"]
        )

        lvl_1_2 = ('countries', 'countries__cities')

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        translations = _get_translations(europe, *lvl_1_2, lang="de")
        dictionary = _get_translations_dictionary(translations)
        hierarchy = _get_relations_hierarchy(*lvl_1_2)

        _apply_entity_translations(europe, hierarchy, dictionary, included=False)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe'
        )
        self.assertEqual(
            europe.denonym,
            'European'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )


class ApplyTranslationsTest(TestCase):
    """Tests for `apply_translations`."""

    # ---- arguments testing -------------------------------------------------

    def test_instance_level_0_relation_no_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        activate("de")

        apply_translations(europe)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_instance_level_1_relation_no_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        activate("de")

        apply_translations(europe, *lvl_1)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_instance_level_2_relation_no_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        activate("de")

        apply_translations(europe, *lvl_2)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )

    def test_instance_level_1_2_relation_no_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        activate("de")

        apply_translations(europe, *lvl_1_2)

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )

    def test_instance_level_0_relation_with_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        apply_translations(europe, lang="de")

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_instance_level_1_relation_with_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        apply_translations(europe, *lvl_1, lang="de")

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_instance_level_2_relation_with_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        apply_translations(europe, *lvl_2, lang="de")

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )

    def test_instance_level_1_2_relation_with_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")

        apply_translations(europe, *lvl_1_2, lang="de")

        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )

    def test_queryset_level_0_relation_no_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2).all()

        activate("de")

        apply_translations(continents)

        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )
        self.assertEqual(
            asia.name,
            'Asien'
        )
        self.assertEqual(
            asia.denonym,
            'Asiatisch'
        )
        self.assertEqual(
            south_korea.name,
            'South Korea'
        )
        self.assertEqual(
            south_korea.denonym,
            'South Korean'
        )
        self.assertEqual(
            seoul.name,
            'Seoul'
        )
        self.assertEqual(
            seoul.denonym,
            'Seouler'
        )

    def test_queryset_level_1_relation_no_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2).all()

        activate("de")

        apply_translations(continents, *lvl_1)

        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )
        self.assertEqual(
            asia.name,
            'Asien'
        )
        self.assertEqual(
            asia.denonym,
            'Asiatisch'
        )
        self.assertEqual(
            south_korea.name,
            'Südkorea'
        )
        self.assertEqual(
            south_korea.denonym,
            'Südkoreanisch'
        )
        self.assertEqual(
            seoul.name,
            'Seoul'
        )
        self.assertEqual(
            seoul.denonym,
            'Seouler'
        )

    def test_queryset_level_2_relation_no_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2).all()

        activate("de")

        apply_translations(continents, *lvl_2)

        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )
        self.assertEqual(
            asia.name,
            'Asien'
        )
        self.assertEqual(
            asia.denonym,
            'Asiatisch'
        )
        self.assertEqual(
            south_korea.name,
            'South Korea'
        )
        self.assertEqual(
            south_korea.denonym,
            'South Korean'
        )
        self.assertEqual(
            seoul.name,
            'Seül'
        )
        self.assertEqual(
            seoul.denonym,
            'Seüler'
        )

    def test_queryset_level_1_2_relation_no_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2).all()

        activate("de")

        apply_translations(continents, *lvl_1_2)

        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )
        self.assertEqual(
            asia.name,
            'Asien'
        )
        self.assertEqual(
            asia.denonym,
            'Asiatisch'
        )
        self.assertEqual(
            south_korea.name,
            'Südkorea'
        )
        self.assertEqual(
            south_korea.denonym,
            'Südkoreanisch'
        )
        self.assertEqual(
            seoul.name,
            'Seül'
        )
        self.assertEqual(
            seoul.denonym,
            'Seüler'
        )

    def test_queryset_level_0_relation_with_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2).all()

        apply_translations(continents, lang="de")

        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )
        self.assertEqual(
            asia.name,
            'Asien'
        )
        self.assertEqual(
            asia.denonym,
            'Asiatisch'
        )
        self.assertEqual(
            south_korea.name,
            'South Korea'
        )
        self.assertEqual(
            south_korea.denonym,
            'South Korean'
        )
        self.assertEqual(
            seoul.name,
            'Seoul'
        )
        self.assertEqual(
            seoul.denonym,
            'Seouler'
        )

    def test_queryset_level_1_relation_with_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2).all()

        apply_translations(continents, *lvl_1, lang="de")

        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )
        self.assertEqual(
            asia.name,
            'Asien'
        )
        self.assertEqual(
            asia.denonym,
            'Asiatisch'
        )
        self.assertEqual(
            south_korea.name,
            'Südkorea'
        )
        self.assertEqual(
            south_korea.denonym,
            'Südkoreanisch'
        )
        self.assertEqual(
            seoul.name,
            'Seoul'
        )
        self.assertEqual(
            seoul.denonym,
            'Seouler'
        )

    def test_queryset_level_2_relation_with_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2).all()

        apply_translations(continents, *lvl_2, lang="de")

        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )
        self.assertEqual(
            asia.name,
            'Asien'
        )
        self.assertEqual(
            asia.denonym,
            'Asiatisch'
        )
        self.assertEqual(
            south_korea.name,
            'South Korea'
        )
        self.assertEqual(
            south_korea.denonym,
            'South Korean'
        )
        self.assertEqual(
            seoul.name,
            'Seül'
        )
        self.assertEqual(
            seoul.denonym,
            'Seüler'
        )

    def test_queryset_level_1_2_relation_with_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2).all()

        apply_translations(continents, *lvl_1_2, lang="de")

        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )
        self.assertEqual(
            asia.name,
            'Asien'
        )
        self.assertEqual(
            asia.denonym,
            'Asiatisch'
        )
        self.assertEqual(
            south_korea.name,
            'Südkorea'
        )
        self.assertEqual(
            south_korea.denonym,
            'Südkoreanisch'
        )
        self.assertEqual(
            seoul.name,
            'Seül'
        )
        self.assertEqual(
            seoul.denonym,
            'Seüler'
        )

    # ---- error testing -----------------------------------------------------

    def test_invalid_lang(self):
        create_samples(
            continent_names=["europe"],
            continent_fields=["name", "denonym"],
            langs=["de"]
        )

        europe = Continent.objects.get(code="EU")

        with self.assertRaises(ValueError) as error:
            apply_translations(
                europe,
                lang="xx"
            )
        self.assertEqual(
            error.exception.args[0],
            "The language code `xx` is not supported."
        )

    def test_invalid_relation(self):
        create_samples(
            continent_names=["europe"],
            continent_fields=["name", "denonym"],
            langs=["de"]
        )

        europe = Continent.objects.get(code="EU")

        with self.assertRaises(FieldDoesNotExist) as error:
            apply_translations(
                europe,
                'wrong',
                lang="de"
            )
        self.assertEqual(
            error.exception.args[0],
            "Continent has no field named 'wrong'"
        )

    def test_invalid_entity(self):
        class Person:
            def __init__(self, name):
                self.name = name

            def __str__(self):
                return self.name

            def __repr__(self):
                return self.name

        behzad = Person('Behzad')
        with self.assertRaises(TypeError) as error:
            apply_translations(
                behzad,
                lang="de"
            )
        self.assertEqual(
            error.exception.args[0],
            "`Behzad` is neither a model instance nor an iterable of model instances."
        )
