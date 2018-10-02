from django.test import TestCase, override_settings
from django.core.exceptions import FieldDoesNotExist

from translations.context import TranslationContext

from sample.models import Continent, Country, City

from tests.sample import create_samples


class TranslationContextTest(TestCase):
    """Tests for `TranslationContext`."""

    @override_settings(LANGUAGE_CODE='de')
    def test_read_instance_level_0_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        europe = Continent.objects.get(code='EU')
        with TranslationContext(europe) as translations:
            translations.read()
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

    @override_settings(LANGUAGE_CODE='de')
    def test_read_instance_level_1_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)

        europe = Continent.objects.get(code='EU')

        with TranslationContext(europe, *lvl_1) as translations:
            translations.read()
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

    @override_settings(LANGUAGE_CODE='de')
    def test_read_instance_level_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)

        europe = Continent.objects.get(code='EU')
        with TranslationContext(europe, *lvl_2) as translations:
            translations.read()
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

    @override_settings(LANGUAGE_CODE='de')
    def test_read_instance_level_1_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.get(code='EU')
        with TranslationContext(europe, *lvl_1_2) as translations:
            translations.read()
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

    def test_read_instance_level_0_relation_with_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        europe = Continent.objects.get(code='EU')
        with TranslationContext(europe) as translations:
            translations.read('de')
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

    def test_read_instance_level_1_relation_with_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)

        europe = Continent.objects.get(code='EU')
        with TranslationContext(europe, *lvl_1) as translations:
            translations.read('de')
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

    def test_read_instance_level_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)

        europe = Continent.objects.get(code='EU')
        with TranslationContext(europe, *lvl_2) as translations:
            translations.read('de')
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

    def test_read_instance_level_1_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.get(code='EU')
        with TranslationContext(europe, *lvl_1_2) as translations:
            translations.read('de')
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

    @override_settings(LANGUAGE_CODE='de')
    def test_read_prefetched_instance_level_0_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with TranslationContext(europe) as translations:
            translations.read()
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

    @override_settings(LANGUAGE_CODE='de')
    def test_read_prefetched_instance_level_1_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with TranslationContext(europe, *lvl_1) as translations:
            translations.read()
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

    @override_settings(LANGUAGE_CODE='de')
    def test_read_prefetched_instance_level_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with TranslationContext(europe, *lvl_2) as translations:
            translations.read()
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

    @override_settings(LANGUAGE_CODE='de')
    def test_read_prefetched_instance_level_1_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with TranslationContext(europe, *lvl_1_2) as translations:
            translations.read()
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

    def test_read_prefetched_instance_level_0_relation_with_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with TranslationContext(europe) as translations:
            translations.read('de')
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

    def test_read_prefetched_instance_level_1_relation_with_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with TranslationContext(europe, *lvl_1) as translations:
            translations.read('de')
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

    def test_read_prefetched_instance_level_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with TranslationContext(europe, *lvl_2) as translations:
            translations.read('de')
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

    def test_read_prefetched_instance_level_1_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with TranslationContext(europe, *lvl_1_2) as translations:
            translations.read('de')
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

    def test_read_instance_invalid_entity(self):
        class Person:
            def __init__(self, name):
                self.name = name

            def __str__(self):
                return self.name

            def __repr__(self):
                return self.name

        behzad = Person('Behzad')

        with self.assertRaises(TypeError) as error:
            with TranslationContext(behzad) as translations:
                translations.read()

        self.assertEqual(
            error.exception.args[0],
            ('`Behzad` is neither a model instance nor an iterable of' +
             ' model instances.')
        )

    def test_read_instance_invalid_simple_relation(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        europe = Continent.objects.get(code='EU')

        with self.assertRaises(FieldDoesNotExist) as error:
            with TranslationContext(europe, 'wrong') as translations:
                translations.read()

        self.assertEqual(
            error.exception.args[0],
            "Continent has no field named 'wrong'"
        )

    def test_read_instance_invalid_nested_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            langs=['de']
        )

        europe = Continent.objects.get(code='EU')

        with self.assertRaises(FieldDoesNotExist) as error:
            with TranslationContext(europe, 'countries__wrong') as translations:
                translations.read()

        self.assertEqual(
            error.exception.args[0],
            "Country has no field named 'wrong'"
        )

    def test_read_instance_invalid_lang(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        europe = Continent.objects.get(code='EU')

        with self.assertRaises(ValueError) as error:
            with TranslationContext(europe) as translations:
                translations.read('xx')

        self.assertEqual(
            error.exception.args[0],
            'The language code `xx` is not supported.'
        )

    @override_settings(LANGUAGE_CODE='de')
    def test_read_queryset_level_0_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.all()
        with TranslationContext(continents) as translations:
            translations.read()
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

    @override_settings(LANGUAGE_CODE='de')
    def test_read_queryset_level_1_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)

        continents = Continent.objects.all()
        with TranslationContext(continents, *lvl_1) as translations:
            translations.read()
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

    @override_settings(LANGUAGE_CODE='de')
    def test_read_queryset_level_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)

        continents = Continent.objects.all()
        with TranslationContext(continents, *lvl_2) as translations:
            translations.read()
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

    @override_settings(LANGUAGE_CODE='de')
    def test_read_queryset_level_1_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.all()
        with TranslationContext(continents, *lvl_1_2) as translations:
            translations.read()
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

    def test_read_queryset_level_0_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.all()
        with TranslationContext(continents) as translations:
            translations.read('de')
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

    def test_read_queryset_level_1_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)

        continents = Continent.objects.all()
        with TranslationContext(continents, *lvl_1) as translations:
            translations.read('de')
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

    def test_read_queryset_level_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)

        continents = Continent.objects.all()
        with TranslationContext(continents, *lvl_2) as translations:
            translations.read('de')
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

    def test_read_queryset_level_1_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.all()
        with TranslationContext(continents, *lvl_1_2) as translations:
            translations.read('de')
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

    @override_settings(LANGUAGE_CODE='de')
    def test_read_prefetched_queryset_level_0_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with TranslationContext(continents) as translations:
            translations.read()
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

    @override_settings(LANGUAGE_CODE='de')
    def test_read_prefetched_queryset_level_1_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with TranslationContext(continents, *lvl_1) as translations:
            translations.read()
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

    @override_settings(LANGUAGE_CODE='de')
    def test_read_prefetched_queryset_level_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with TranslationContext(continents, *lvl_2) as translations:
            translations.read()
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

    @override_settings(LANGUAGE_CODE='de')
    def test_read_prefetched_queryset_level_1_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with TranslationContext(continents, *lvl_1_2) as translations:
            translations.read()
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

    def test_read_prefetched_queryset_level_0_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with TranslationContext(continents) as translations:
            translations.read('de')
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

    def test_read_prefetched_queryset_level_1_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with TranslationContext(continents, *lvl_1) as translations:
            translations.read('de')
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

    def test_read_prefetched_queryset_level_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with TranslationContext(continents, *lvl_2) as translations:
            translations.read('de')
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

    def test_read_prefetched_queryset_level_1_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with TranslationContext(continents, *lvl_1_2) as translations:
            translations.read('de')
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

    def test_read_queryset_invalid_entity(self):
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
            with TranslationContext(people) as translations:
                translations.read()

        self.assertEqual(
            error.exception.args[0],
            ('`[Behzad, Max]` is neither a model instance nor an iterable of' +
             ' model instances.')
        )

    def test_read_queryset_invalid_simple_relation(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        continents = Continent.objects.all()

        with self.assertRaises(FieldDoesNotExist) as error:
            with TranslationContext(continents, 'wrong') as translations:
                translations.read()

        self.assertEqual(
            error.exception.args[0],
            "Continent has no field named 'wrong'"
        )

    def test_read_queryset_invalid_nested_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            langs=['de']
        )

        continents = Continent.objects.all()

        with self.assertRaises(FieldDoesNotExist) as error:
            with TranslationContext(continents, 'countries__wrong') as translations:
                translations.read()

        self.assertEqual(
            error.exception.args[0],
            "Country has no field named 'wrong'"
        )

    def test_read_queryset_invalid_lang(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        continents = Continent.objects.all()

        with self.assertRaises(ValueError) as error:
            with TranslationContext(continents) as translations:
                translations.read('xx')

        self.assertEqual(
            error.exception.args[0],
            'The language code `xx` is not supported.'
        )

    @override_settings(LANGUAGE_CODE='de')
    def test_update_instance_level_0_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with TranslationContext(europe, *lvl_1_2) as translations:
            translations.read()

            # change
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            translations.update()

            # reapply
            translations.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
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

    @override_settings(LANGUAGE_CODE='de')
    def test_update_instance_level_1_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with TranslationContext(europe, *lvl_1_2) as translations:
            translations.read()

            # change
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            translations.update()

            # reapply
            translations.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
        )
        self.assertEqual(
            germany.name,
            'Germany Name'
        )
        self.assertEqual(
            germany.denonym,
            'Germany Denonym'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )

    @override_settings(LANGUAGE_CODE='de')
    def test_update_instance_level_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with TranslationContext(europe, *lvl_1_2) as translations:
            translations.read()

            # change
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'
            translations.update()

            # reapply
            translations.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
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
            'Cologne Name'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologne Denonym'
        )

    @override_settings(LANGUAGE_CODE='de')
    def test_update_instance_level_1_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with TranslationContext(europe, *lvl_1_2) as translations:
            translations.read()

            # change
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'
            translations.update()

            # reapply
            translations.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
        )
        self.assertEqual(
            germany.name,
            'Germany Name'
        )
        self.assertEqual(
            germany.denonym,
            'Germany Denonym'
        )
        self.assertEqual(
            cologne.name,
            'Cologne Name'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologne Denonym'
        )

    def test_update_instance_level_0_relation_with_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with TranslationContext(europe, *lvl_1_2) as translations:
            translations.read('de')

            # change
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            translations.update('de')

            # reapply
            translations.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
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

    def test_update_instance_level_1_relation_with_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with TranslationContext(europe, *lvl_1_2) as translations:
            translations.read('de')

            # change
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            translations.update('de')

            # reapply
            translations.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
        )
        self.assertEqual(
            germany.name,
            'Germany Name'
        )
        self.assertEqual(
            germany.denonym,
            'Germany Denonym'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )

    def test_update_instance_level_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with TranslationContext(europe, *lvl_1_2) as translations:
            translations.read('de')

            # change
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'
            translations.update('de')

            # reapply
            translations.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
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
            'Cologne Name'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologne Denonym'
        )

    def test_update_instance_level_1_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with TranslationContext(europe, *lvl_1_2) as translations:
            translations.read('de')

            # change
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'
            translations.update('de')

            # reapply
            translations.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
        )
        self.assertEqual(
            germany.name,
            'Germany Name'
        )
        self.assertEqual(
            germany.denonym,
            'Germany Denonym'
        )
        self.assertEqual(
            cologne.name,
            'Cologne Name'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologne Denonym'
        )

    def test_update_instance_invalid_entity(self):
        class Person:
            def __init__(self, name):
                self.name = name

            def __str__(self):
                return self.name

            def __repr__(self):
                return self.name

        behzad = Person('Behzad')

        with self.assertRaises(TypeError) as error:
            with TranslationContext(behzad) as translations:
                translations.update(behzad)

        self.assertEqual(
            error.exception.args[0],
            ('`Behzad` is neither a model instance nor an iterable of' +
             ' model instances.')
        )

    def test_update_instance_invalid_simple_relation(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        europe = Continent.objects.get(code='EU')

        with self.assertRaises(FieldDoesNotExist) as error:
            with TranslationContext(europe, 'wrong') as translations:
                translations.update()

        self.assertEqual(
            error.exception.args[0],
            "Continent has no field named 'wrong'"
        )

    def test_update_instance_invalid_nested_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            langs=['de']
        )

        lvl_1 = ('countries',)

        europe = Continent.objects.prefetch_related(*lvl_1).get(code='EU')

        with self.assertRaises(FieldDoesNotExist) as error:
            with TranslationContext(europe, 'countries__wrong') as translations:
                translations.update()

        self.assertEqual(
            error.exception.args[0],
            "Country has no field named 'wrong'"
        )

    def test_update_instance_invalid_lang(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        europe = Continent.objects.get(code='EU')

        with self.assertRaises(ValueError) as error:
            with TranslationContext(europe) as translations:
                translations.update('xx')

        self.assertEqual(
            error.exception.args[0],
            'The language code `xx` is not supported.'
        )

    @override_settings(LANGUAGE_CODE='de')
    def test_update_queryset_level_0_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with TranslationContext(continents, *lvl_1_2) as translations:
            translations.read()

            # change
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]
            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            asia.name = 'Asia Name'
            asia.denonym = 'Asia Denonym'
            translations.update()

            # reapply
            translations.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
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
            'Asia Name'
        )
        self.assertEqual(
            asia.denonym,
            'Asia Denonym'
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

    @override_settings(LANGUAGE_CODE='de')
    def test_update_queryset_level_1_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with TranslationContext(continents, *lvl_1_2) as translations:
            translations.read()

            # change
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]
            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            asia.name = 'Asia Name'
            asia.denonym = 'Asia Denonym'
            south_korea.name = 'South Korea Name'
            south_korea.denonym = 'South Korea Denonym'
            translations.update()

            # reapply
            translations.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
        )
        self.assertEqual(
            germany.name,
            'Germany Name'
        )
        self.assertEqual(
            germany.denonym,
            'Germany Denonym'
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
            'Asia Name'
        )
        self.assertEqual(
            asia.denonym,
            'Asia Denonym'
        )
        self.assertEqual(
            south_korea.name,
            'South Korea Name'
        )
        self.assertEqual(
            south_korea.denonym,
            'South Korea Denonym'
        )
        self.assertEqual(
            seoul.name,
            'Seül'
        )
        self.assertEqual(
            seoul.denonym,
            'Seüler'
        )

    @override_settings(LANGUAGE_CODE='de')
    def test_update_queryset_level_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with TranslationContext(continents, *lvl_1_2) as translations:
            translations.read()

            # change
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]
            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'
            asia.name = 'Asia Name'
            asia.denonym = 'Asia Denonym'
            seoul.name = 'Seoul Name'
            seoul.denonym = 'Seoul Denonym'
            translations.update()

            # reapply
            translations.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
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
            'Cologne Name'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologne Denonym'
        )
        self.assertEqual(
            asia.name,
            'Asia Name'
        )
        self.assertEqual(
            asia.denonym,
            'Asia Denonym'
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
            'Seoul Name'
        )
        self.assertEqual(
            seoul.denonym,
            'Seoul Denonym'
        )

    @override_settings(LANGUAGE_CODE='de')
    def test_update_queryset_level_1_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with TranslationContext(continents, *lvl_1_2) as translations:
            translations.read()

            # change
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]
            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'
            asia.name = 'Asia Name'
            asia.denonym = 'Asia Denonym'
            south_korea.name = 'South Korea Name'
            south_korea.denonym = 'South Korea Denonym'
            seoul.name = 'Seoul Name'
            seoul.denonym = 'Seoul Denonym'
            translations.update()

            # reapply
            translations.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
        )
        self.assertEqual(
            germany.name,
            'Germany Name'
        )
        self.assertEqual(
            germany.denonym,
            'Germany Denonym'
        )
        self.assertEqual(
            cologne.name,
            'Cologne Name'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologne Denonym'
        )
        self.assertEqual(
            asia.name,
            'Asia Name'
        )
        self.assertEqual(
            asia.denonym,
            'Asia Denonym'
        )
        self.assertEqual(
            south_korea.name,
            'South Korea Name'
        )
        self.assertEqual(
            south_korea.denonym,
            'South Korea Denonym'
        )
        self.assertEqual(
            seoul.name,
            'Seoul Name'
        )
        self.assertEqual(
            seoul.denonym,
            'Seoul Denonym'
        )

    def test_update_queryset_level_0_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with TranslationContext(continents, *lvl_1_2) as translations:
            translations.read('de')

            # change
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]
            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            asia.name = 'Asia Name'
            asia.denonym = 'Asia Denonym'
            translations.update('de')

            # reapply
            translations.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
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
            'Asia Name'
        )
        self.assertEqual(
            asia.denonym,
            'Asia Denonym'
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

    def test_update_queryset_level_1_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with TranslationContext(continents, *lvl_1_2) as translations:
            translations.read('de')

            # change
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]
            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            asia.name = 'Asia Name'
            asia.denonym = 'Asia Denonym'
            south_korea.name = 'South Korea Name'
            south_korea.denonym = 'South Korea Denonym'
            translations.update('de')

            # reapply
            translations.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
        )
        self.assertEqual(
            germany.name,
            'Germany Name'
        )
        self.assertEqual(
            germany.denonym,
            'Germany Denonym'
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
            'Asia Name'
        )
        self.assertEqual(
            asia.denonym,
            'Asia Denonym'
        )
        self.assertEqual(
            south_korea.name,
            'South Korea Name'
        )
        self.assertEqual(
            south_korea.denonym,
            'South Korea Denonym'
        )
        self.assertEqual(
            seoul.name,
            'Seül'
        )
        self.assertEqual(
            seoul.denonym,
            'Seüler'
        )

    def test_update_queryset_level_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with TranslationContext(continents, *lvl_1_2) as translations:
            translations.read('de')

            # change
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]
            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'
            asia.name = 'Asia Name'
            asia.denonym = 'Asia Denonym'
            seoul.name = 'Seoul Name'
            seoul.denonym = 'Seoul Denonym'
            translations.update('de')

            # reapply
            translations.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
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
            'Cologne Name'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologne Denonym'
        )
        self.assertEqual(
            asia.name,
            'Asia Name'
        )
        self.assertEqual(
            asia.denonym,
            'Asia Denonym'
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
            'Seoul Name'
        )
        self.assertEqual(
            seoul.denonym,
            'Seoul Denonym'
        )

    def test_update_queryset_level_1_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with TranslationContext(continents, *lvl_1_2) as translations:
            translations.read('de')

            # change
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]
            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'
            asia.name = 'Asia Name'
            asia.denonym = 'Asia Denonym'
            south_korea.name = 'South Korea Name'
            south_korea.denonym = 'South Korea Denonym'
            seoul.name = 'Seoul Name'
            seoul.denonym = 'Seoul Denonym'
            translations.update('de')

            # reapply
            translations.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
        )
        self.assertEqual(
            germany.name,
            'Germany Name'
        )
        self.assertEqual(
            germany.denonym,
            'Germany Denonym'
        )
        self.assertEqual(
            cologne.name,
            'Cologne Name'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologne Denonym'
        )
        self.assertEqual(
            asia.name,
            'Asia Name'
        )
        self.assertEqual(
            asia.denonym,
            'Asia Denonym'
        )
        self.assertEqual(
            south_korea.name,
            'South Korea Name'
        )
        self.assertEqual(
            south_korea.denonym,
            'South Korea Denonym'
        )
        self.assertEqual(
            seoul.name,
            'Seoul Name'
        )
        self.assertEqual(
            seoul.denonym,
            'Seoul Denonym'
        )

    def test_update_queryset_invalid_entity(self):
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
            with TranslationContext(people) as translations:
                translations.update(people)

        self.assertEqual(
            error.exception.args[0],
            ('`[Behzad, Max]` is neither a model instance nor an iterable of' +
             ' model instances.')
        )

    def test_update_queryset_invalid_simple_relation(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        continents = Continent.objects.all()

        with self.assertRaises(FieldDoesNotExist) as error:
            with TranslationContext(continents, 'wrong') as translations:
                translations.update()

        self.assertEqual(
            error.exception.args[0],
            "Continent has no field named 'wrong'"
        )

    def test_update_queryset_invalid_nested_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            langs=['de']
        )

        lvl_1 = ('countries',)

        continents = Continent.objects.prefetch_related(*lvl_1)

        with self.assertRaises(FieldDoesNotExist) as error:
            with TranslationContext(continents, 'countries__wrong') as translations:
                translations.update()

        self.assertEqual(
            error.exception.args[0],
            "Country has no field named 'wrong'"
        )

    def test_update_queryset_invalid_lang(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        continents = Continent.objects.all()

        with self.assertRaises(ValueError) as error:
            with TranslationContext(continents) as translations:
                translations.update('xx')

        self.assertEqual(
            error.exception.args[0],
            'The language code `xx` is not supported.'
        )
